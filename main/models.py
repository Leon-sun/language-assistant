from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from typing import Dict, Optional, Tuple
import json
from .interest_graph import Interest


class GlobalWord(models.Model):
    """
    Global word entry independent of any user.
    Represents the dictionary entry itself.
    """
    text = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="The word text (French or English)"
    )
    language = models.CharField(
        max_length=10,
        default='fr',
        help_text="Language of the word (e.g., 'fr', 'en')"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['text']
        verbose_name = 'Global Word'
        verbose_name_plural = 'Global Words'
        indexes = [
            models.Index(fields=['text']),
            models.Index(fields=['language', 'text']),
        ]
    
    def __str__(self):
        return f"{self.text} ({self.language})"


class ContentCard(models.Model):
    """
    Stores Gemini-generated content with meta-tags for reuse.
    Multiple users can reference the same ContentCard.
    """
    CEFR_LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient'),
    ]
    
    word = models.ForeignKey(
        GlobalWord,
        on_delete=models.CASCADE,
        related_name='content_cards',
        help_text="Reference to the global word"
    )
    definition = models.TextField(
        help_text="Gemini-generated definition/explanation"
    )
    conversation = models.TextField(
        blank=True,
        null=True,
        help_text="Personalized dialogue or conversation context"
    )
    examples = models.TextField(
        help_text="JSON-encoded examples (stored as text for SQLite compatibility)"
    )
    
    # Reuse Meta-Tags (The Index)
    target_language = models.CharField(
        max_length=10,
        default='fr',
        help_text="Target language for this content (e.g., 'fr', 'en', 'es')"
    )
    target_cefr = models.CharField(
        max_length=2,
        choices=CEFR_LEVEL_CHOICES,
        help_text="Target CEFR level for this content"
    )
    interest_context = models.CharField(
        max_length=100,
        default='General',
        help_text="Interest context (e.g., 'Hockey', 'Cooking', 'General')"
    )
    tone_style = models.CharField(
        max_length=50,
        default='Neutral',
        help_text="Tone/style (e.g., 'Dark Humor', 'Academic', 'Neutral')"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Content Card'
        verbose_name_plural = 'Content Cards'
        ordering = ['-created_at']
        # Composite index for fast lookups (including target_language)
        indexes = [
            models.Index(fields=['word', 'target_language', 'target_cefr', 'interest_context', 'tone_style']),
        ]
        # Ensure uniqueness of content for same meta-tags (including target_language)
        unique_together = [('word', 'target_language', 'target_cefr', 'interest_context', 'tone_style')]
    
    def __str__(self):
        return f"{self.word.text} ({self.target_language}) - {self.target_cefr} ({self.interest_context}, {self.tone_style})"
    
    def get_examples(self) -> list:
        """Parse and return examples as a list."""
        try:
            return json.loads(self.examples) if self.examples else []
        except json.JSONDecodeError:
            return []
    
    def set_examples(self, examples_list: list):
        """Set examples from a list."""
        self.examples = json.dumps(examples_list) if examples_list else '[]'


class UserVocabulary(models.Model):
    """
    Represents a user's saved words list.
    Links users to ContentCards (many users can share the same card).
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vocabulary',
        help_text="User who saved this word"
    )
    card = models.ForeignKey(
        ContentCard,
        on_delete=models.CASCADE,
        related_name='user_vocabularies',
        help_text="Content card for this word"
    )
    familiarity = models.IntegerField(
        default=1,
        help_text="Familiarity level from 1-5 (1 = new, 5 = mastered)"
    )
    added_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Vocabulary'
        verbose_name_plural = 'User Vocabularies'
        ordering = ['-added_at']
        # Ensure a user can only have one entry per card
        unique_together = [('user', 'card')]
        indexes = [
            models.Index(fields=['user', '-added_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.card.word.text}"


class Word(models.Model):
    """Model to store dictionary words with their translations and examples."""
    
    CEFR_LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient'),
    ]
    
    # User association
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='words',
        help_text="User who saved this word",
        null=True,
        blank=True,
    )
    
    # Basic word information
    original_word = models.CharField(max_length=200, help_text="The word entered by user (French or English)")
    french_word = models.CharField(max_length=200, help_text="French word in basic form")
    english_translation = models.TextField(help_text="English explanation/translation")
    french_explanation = models.TextField(help_text="French explanation")
    
    # Examples (stored as JSON-like text, can be upgraded to JSONField in future)
    english_examples = models.TextField(help_text="3 English usage examples (one per line)")
    french_examples = models.TextField(help_text="3 French usage examples (one per line)")
    
    # Metadata
    cefr_level = models.CharField(
        max_length=2,
        choices=CEFR_LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text="CEFR level (A1, A2, B1, B2, C1, C2) as determined by Gemini"
    )
    familiarity = models.IntegerField(
        default=1,
        help_text="Familiarity level from 1-5 (1 = new, 5 = mastered)"
    )
    
    # Keep difficulty_level for backward compatibility (deprecated)
    difficulty_level = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Deprecated: Use cefr_level instead"
    )
    
    # OpenAI prompt used (for reference)
    openai_prompt = models.TextField(blank=True, null=True, help_text="The prompt used for OpenAI API")
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
    
    def __str__(self):
        return f"{self.french_word} ({self.original_word})"


class InterestCategory(models.Model):
    """Category for organizing interest tags."""
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="URL-friendly identifier"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Interest Category'
        verbose_name_plural = 'Interest Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class InterestTag(models.Model):
    """Tag representing a specific interest."""
    category = models.ForeignKey(
        InterestCategory,
        on_delete=models.CASCADE,
        related_name='tags',
        help_text="Category this tag belongs to"
    )
    name = models.CharField(
        max_length=100,
        help_text="Tag name"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="URL-friendly identifier"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order within category"
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Interest Tag'
        verbose_name_plural = 'Interest Tags'
        ordering = ['category__order', 'category__name', 'order', 'name']
        unique_together = [('category', 'name')]
        indexes = [
            models.Index(fields=['category', 'order']),
        ]
    
    def __str__(self):
        return f"{self.category.name}: {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """User profile model with level, interest, and contact information."""
    
    LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient'),
    ]
    
    AGE_GROUP_CHOICES = [
        ('early_childhood', 'Early Childhood'),
        ('early_elementary', 'Early Elementary'),
        ('upper_elementary', 'Upper Elementary'),
        ('middle_school', 'Middle School'),
        ('high_school', 'High School'),
        ('adult', 'Adult'),
        ('senior', 'Senior'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('zh', 'Chinese (Mandarin)'),
        ('ja', 'Japanese'),
        ('fr', 'French'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="Link to Django User model"
    )
    nickname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="User's nickname or display name"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="User's profile picture"
    )
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text="User's French proficiency level (CEFR)"
    )
    age_group = models.CharField(
        max_length=20,
        choices=AGE_GROUP_CHOICES,
        blank=True,
        null=True,
        help_text="User's age group or education level"
    )
    # Keep old interest field temporarily for data migration
    interest = models.TextField(
        blank=True,
        null=True,
        help_text="DEPRECATED: Use interests (tags) instead. Kept for migration purposes."
    )
    interests = models.ManyToManyField(
        InterestTag,
        blank=True,
        related_name='users',
        help_text="User's selected interest tags"
    )
    learning_goals = models.TextField(
        blank=True,
        null=True,
        help_text="Free-form learning goals and notes"
    )
    contact = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Contact information (email, phone, etc.)"
    )
    target_language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='fr',
        help_text="Language the user is learning"
    )
    native_language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en',
        help_text="Language used for explanations/definitions"
    )
    # Store interests as JSON (for SQLite compatibility, using TextField)
    interests_data = models.TextField(
        blank=True,
        null=True,
        help_text="JSON data for weighted interest graph",
        default='{}'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    @property
    def interest_graph(self) -> Dict[str, Interest]:
        """
        Get interest graph dictionary mapping label -> Interest object.
        Lazy-loads from JSON storage.
        This is the weighted interest graph, separate from the ManyToMany interests field.
        """
        if not self.interests_data:
            return {}
        
        try:
            data = json.loads(self.interests_data)
            return {
                label: Interest.from_dict(interest_data)
                for label, interest_data in data.items()
            }
        except (json.JSONDecodeError, KeyError, ValueError):
            return {}
    
    @interest_graph.setter
    def interest_graph(self, value: Dict[str, Interest]):
        """Set interest graph dictionary, serializing to JSON."""
        if not isinstance(value, dict):
            raise ValueError("Interest graph must be a dictionary")
        
        # Convert Interest objects to dictionaries
        serialized = {
            label: interest.to_dict()
            for label, interest in value.items()
        }
        
        self.interests_data = json.dumps(serialized)
    
    def record_interaction(self, label: str, action_type: str) -> None:
        """
        Record an interaction and update the interest score.
        
        Process:
        1. Lazy Decay: Calculate decay based on time difference
        2. Add Weight: Add points based on action_type
        3. Normalization: Ensure score never exceeds 1.0
        
        Args:
            label: Interest label (str)
            action_type: Type of action ('click', 'view_50_percent', 'view_100_percent', 'share', 'explicit_tag')
        """
        # Action type weights
        action_weights = {
            'click': 0.1,
            'view_50_percent': 0.3,
            'view_100_percent': 0.5,
            'share': 0.8,
            'explicit_tag': 1.0
        }
        
        if action_type not in action_weights:
            raise ValueError(
                f"Invalid action_type '{action_type}'. "
                f"Must be one of: {list(action_weights.keys())}"
            )
        
        weight = action_weights[action_type]
        current_time = timezone.now()
        
        # Get current interests
        interests_dict = self.interest_graph
        
        # Step 1: Lazy Decay - if interest exists, apply decay first
        if label in interests_dict:
            interest = interests_dict[label]
            # Apply decay based on time difference
            interest.score = interest.decay_score(current_time)
        else:
            # Create new interest
            interest = Interest(label=label, score=0.0, last_updated=current_time)
        
        # Step 2: Add Weight
        interest.score += weight
        
        # Step 3: Normalization - ensure score never exceeds 1.0
        interest.score = min(1.0, interest.score)
        
        # Update metadata
        interest.last_updated = current_time
        interest.interaction_count += 1
        
        # Save back to dictionary
        interests_dict[label] = interest
        
        # Update the stored JSON
        self.interest_graph = interests_dict


class Article(models.Model):
    """Model to store articles from RSS feeds."""
    
    title = models.CharField(
        max_length=500,
        help_text="Article title from RSS feed"
    )
    content = models.TextField(
        help_text="Article content"
    )
    date = models.DateTimeField(
        help_text="Publication date from RSS feed"
    )
    label = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Label or category for the article"
    )
    source_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Original URL of the article"
    )
    rss_feed_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="RSS feed URL where this article was found"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['label']),
        ]
    
    def __str__(self):
        return f"{self.title[:50]}..." if len(self.title) > 50 else self.title
