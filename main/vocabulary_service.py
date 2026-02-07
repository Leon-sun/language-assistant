"""
Service for fetching word content with reusable personalized cache.
"""
import logging
from typing import Dict, Optional, Tuple
from django.contrib.auth.models import User
from django.utils import timezone
from .models import GlobalWord, ContentCard, UserVocabulary
from .services import lookup_word
import json

logger = logging.getLogger(__name__)


def get_user_top_interest(user: User) -> str:
    """
    Get the user's top interest based on their interest graph.
    
    Args:
        user: Django User instance
    
    Returns:
        str: Top interest label or 'General' if none found
    """
    try:
        if hasattr(user, 'profile') and user.profile:
            interests = user.profile.interest_graph
            if interests:
                # Get interest with highest score
                top_interest = max(interests.items(), key=lambda x: x[1].score)
                return top_interest[0]
    except Exception as e:
        logger.warning(f"Error getting user top interest: {str(e)}")
    
    return 'General'


def get_user_preferred_tone(user: User) -> str:
    """
    Get the user's preferred tone/style.
    This could be extended to track user preferences.
    
    Args:
        user: Django User instance
    
    Returns:
        str: Preferred tone/style, default 'Neutral'
    """
    # For now, return default. Can be extended to read from user preferences
    return 'Neutral'


def get_user_cefr_level(user: User) -> str:
    """
    Get the user's CEFR level from their profile.
    
    Args:
        user: Django User instance
    
    Returns:
        str: CEFR level (A1-C2) or 'A1' as default
    """
    try:
        if hasattr(user, 'profile') and user.profile:
            level = user.profile.level
            if level:
                return level
    except Exception as e:
        logger.warning(f"Error getting user CEFR level: {str(e)}")
    
    return 'A1'  # Default to A1


def fetch_word_content(user: User, word_text: str) -> Tuple[ContentCard, UserVocabulary]:
    """
    Fetch word content with reusable personalized cache.
    
    Process:
    A) Check if GlobalWord exists, create if not
    B) Look for existing ContentCard matching user's level, interest, tone
    C) If match found -> reuse; if not -> call Gemini and create new card
    D) Create/Get UserVocabulary entry linking user to the card
    
    Args:
        user: Django User instance
        word_text: The word to fetch content for
    
    Returns:
        tuple: (ContentCard, UserVocabulary) instances
    """
    # Step A: Get user's language preferences
    target_language = 'fr'
    if user.is_authenticated and hasattr(user, 'profile') and user.profile:
        target_language = getattr(user.profile, 'target_language', 'fr') or 'fr'
    
    # Get or create GlobalWord with target language
    global_word, created = GlobalWord.objects.get_or_create(
        text=word_text.strip().lower(),
        defaults={'language': target_language}
    )
    if created:
        logger.info(f"Created new GlobalWord: {word_text} (language: {target_language})")
    elif global_word.language != target_language:
        # Update language if it changed
        global_word.language = target_language
        global_word.save()
    
    # Step B: Get user's preferences
    target_cefr = get_user_cefr_level(user)
    interest_context = get_user_top_interest(user)
    tone_style = get_user_preferred_tone(user)
    
    # Look for existing ContentCard with matching meta-tags (including target_language)
    content_card = ContentCard.objects.filter(
        word=global_word,
        target_language=target_language,
        target_cefr=target_cefr,
        interest_context=interest_context,
        tone_style=tone_style
    ).first()
    
    # Step C: If no match, create new ContentCard by calling Gemini
    if not content_card:
        logger.info(
            f"No matching ContentCard found for {word_text} "
            f"(Language: {target_language}, CEFR: {target_cefr}, Interest: {interest_context}, Tone: {tone_style}). "
            f"Calling Gemini to create new card."
        )
        
        try:
            # Get user profile for personalization
            user_profile = None
            if user.is_authenticated and hasattr(user, 'profile'):
                user_profile = user.profile
            
            # Call Gemini to get word content (pass user profile for personalization)
            word_data = lookup_word(word_text, user_profile=user_profile)
            
            # Extract data from Gemini response (new format with language-agnostic fields)
            definition = word_data.get('explanation_native', '') or word_data.get('personalized_explanation', '') or word_data.get('definition_en', '')
            conversation = word_data.get('conversation_target', '') or word_data.get('conversation_fr', '')
            examples = word_data.get('usages_target', []) or word_data.get('usages_fr', [])
            cefr_level = word_data.get('difficulty_level', '') or word_data.get('cefr_level', target_cefr)
            result_target_language = word_data.get('target_language', target_language)
            
            # Create new ContentCard
            content_card = ContentCard.objects.create(
                word=global_word,
                definition=definition,
                conversation=conversation,
                examples=json.dumps(examples) if examples else '[]',
                target_language=result_target_language,
                target_cefr=cefr_level if cefr_level in dict(ContentCard.CEFR_LEVEL_CHOICES) else target_cefr,
                interest_context=interest_context,
                tone_style=tone_style
            )
            
            logger.info(f"Created new ContentCard: {content_card}")
            
        except Exception as e:
            logger.error(f"Error calling Gemini for word '{word_text}': {str(e)}")
            # Create a fallback card with minimal content
            content_card = ContentCard.objects.create(
                word=global_word,
                definition=f"Definition for {word_text}",
                conversation='',
                examples='[]',
                target_language=target_language,
                target_cefr=target_cefr,
                interest_context=interest_context,
                tone_style=tone_style
            )
    else:
        logger.info(f"Reusing existing ContentCard: {content_card}")
    
    # Step D: Create or get UserVocabulary entry
    user_vocab, created = UserVocabulary.objects.get_or_create(
        user=user,
        card=content_card,
        defaults={'familiarity': 1}
    )
    
    if created:
        logger.info(f"Created new UserVocabulary entry for user {user.username}")
    else:
        logger.debug(f"UserVocabulary entry already exists for user {user.username}")
    
    return content_card, user_vocab
