from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from .models import Word, Article, UserProfile
from .forms import WordLookupForm, WordForm, ProfileSettingsForm
from .services import lookup_word
from .rss_service import parse_rss_feeds
import json
import traceback
import feedparser
import logging

logger = logging.getLogger(__name__)


def index(request):
    """Home page view."""
    return render(request, 'main/index.html')


def about(request):
    """About page view."""
    return render(request, 'main/about.html')


def word_lookup(request):
    """View for looking up and translating words."""
    lookup_form = WordLookupForm()
    word_data = None
    
    if request.method == 'POST':
        if 'lookup_word' in request.POST:
            lookup_form = WordLookupForm(request.POST)
            if lookup_form.is_valid():
                word = lookup_form.cleaned_data['word'].strip()
                if not word:
                    messages.error(request, "Please enter a word to lookup.")
                else:
                    try:
                        # Get user profile if authenticated
                        user_profile = None
                        if request.user.is_authenticated and hasattr(request.user, 'profile'):
                            user_profile = request.user.profile
                        
                        # Call Gemini service with robust error handling
                        word_data = lookup_word(word, user_profile=user_profile)
                        # Keep original_word for display purposes
                        if 'original_word' not in word_data:
                            word_data['original_word'] = word
                        if 'input_word' not in word_data:
                            word_data['input_word'] = word
                    except ValueError as e:
                        # Handle validation and parsing errors
                        error_msg = str(e)
                        messages.error(request, f"Error looking up word: {error_msg}")
                    except Exception as e:
                        # Handle unexpected errors
                        error_msg = f"Unexpected error: {str(e)}"
                        if settings.DEBUG:
                            error_msg += f"\n{traceback.format_exc()}"
                        messages.error(request, error_msg)
        
        elif 'save_word' in request.POST:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                messages.warning(request, "Please sign in to save words. You can still look up words without signing in.")
            else:
                # Save the word to database
                word_json = request.POST.get('word_data')
                if word_json:
                    try:
                        data = json.loads(word_json)
                        # Map Gemini response structure to Word model fields
                        # Support both new schema (usages_target) and legacy (usages_fr)
                        usages = data.get('usages_target', []) or data.get('usages_fr', [])
                        if not isinstance(usages, list):
                            usages = []
                        
                        # Get the original word (user input) - try multiple sources
                        original_word = (
                            data.get('input_word') or 
                            data.get('original_word') or 
                            (word_data.get('input_word') if word_data else None) or
                            (word_data.get('original_word') if word_data else None) or
                            ''
                        )
                        
                        # Get definition/explanation (support both new and legacy keys)
                        definition = (
                            data.get('explanation_native', '') or 
                            data.get('personalized_explanation', '') or 
                            data.get('definition_en', '')
                        )
                        
                        # Get CEFR level (support both new and legacy keys)
                        cefr_level = data.get('difficulty_level', '') or data.get('cefr_level', '')
                        
                        # Create Word object with proper field mapping
                        # Automatically set familiarity to 1 (scale 1-5)
                        # Get CEFR level from Gemini response
                        word_obj = Word.objects.create(
                            user=request.user,  # Associate word with logged-in user
                            original_word=original_word,
                            french_word=data.get('base_form', ''),
                            english_translation=definition,
                            french_explanation='',  # Leave blank for now
                            english_examples='',  # Leave blank for now
                            french_examples='\n'.join(usages) if usages else '',
                            cefr_level=cefr_level,  # From Gemini
                            familiarity=1,  # Automatically set to 1 (scale 1-5)
                            openai_prompt='',  # Prompt not stored
                        )
                        messages.success(request, f"Word '{word_obj.french_word}' saved successfully!")
                        return redirect('word_list')
                    except json.JSONDecodeError as e:
                        # If parsing fails, try to get word_data from session or keep existing
                        messages.warning(request, f"Could not save word (parsing error): {str(e)}. The lookup result is still displayed above.")
                    except Exception as e:
                        # Graceful error handling - show warning but don't crash
                        # Keep word_data so the lookup result is still displayed
                        error_msg = str(e)
                        if 'no such table' in error_msg.lower():
                            messages.warning(request, "Database table not found. Please run migrations: python manage.py migrate")
                        else:
                            messages.warning(request, f"Could not save word: {error_msg}. The lookup result is still displayed above.")
                else:
                    # If no word_json, try to use word_data if available
                    if word_data:
                        messages.warning(request, "Could not save word: missing data. The lookup result is still displayed above.")
    
    context = {
        'lookup_form': lookup_form,
        'word_data': word_data,
    }
    return render(request, 'main/word_lookup.html', context)


def word_list(request):
    """View for displaying the list of saved words."""
    # Only show words for authenticated users
    if request.user.is_authenticated:
        words = Word.objects.filter(user=request.user)
    else:
        words = Word.objects.none()  # Empty queryset for non-authenticated users
    
    # Filter by CEFR level if provided
    cefr_level = request.GET.get('cefr_level', '')
    if cefr_level:
        words = words.filter(cefr_level=cefr_level)
    
    # Filter by familiarity if provided
    familiarity = request.GET.get('familiarity', '')
    if familiarity:
        words = words.filter(familiarity=familiarity)
    
    context = {
        'words': words,
        'cefr_level_filter': cefr_level,
        'familiarity_filter': familiarity,
    }
    return render(request, 'main/word_list.html', context)


def word_detail(request, word_id):
    """View for displaying detailed information about a word."""
    # Only allow users to view their own words
    if request.user.is_authenticated:
        word = get_object_or_404(Word, id=word_id, user=request.user)
    else:
        messages.error(request, "Please sign in to view word details.")
        return redirect('word_list')
    
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            messages.success(request, "Word updated successfully!")
            return redirect('word_detail', word_id=word.id)
    else:
        form = WordForm(instance=word)
    
    context = {
        'word': word,
        'form': form,
        'english_examples': word.english_examples.split('\n') if word.english_examples else [],
        'french_examples': word.french_examples.split('\n') if word.french_examples else [],
    }
    return render(request, 'main/word_detail.html', context)


def word_delete(request, word_id):
    """View for deleting a word."""
    # Only allow users to delete their own words
    if request.user.is_authenticated:
        word = get_object_or_404(Word, id=word_id, user=request.user)
    else:
        messages.error(request, "Please sign in to delete words.")
        return redirect('word_list')
    
    if request.method == 'POST':
        word.delete()
        messages.success(request, f"Word '{word.french_word}' deleted successfully!")
        return redirect('word_list')
    return render(request, 'main/word_delete.html', {'word': word})


def stories(request):
    """View for displaying stories from RSS feeds."""
    from datetime import datetime
    
    # Le Monde RSS feed URLs
    rss_urls = [
        'https://www.lemonde.fr/rss/une.xml',
        'https://www.lemonde.fr/economie/rss_full.xml',
        'https://www.lemonde.fr/culture/rss_full.xml',
        'https://www.lemonde.fr/idees/rss_full.xml',
    ]
    
    # Feed labels
    feed_labels = {
        'https://www.lemonde.fr/rss/une.xml': 'Actualités',
        'https://www.lemonde.fr/economie/rss_full.xml': 'Économie',
        'https://www.lemonde.fr/culture/rss_full.xml': 'Culture',
        'https://www.lemonde.fr/idees/rss_full.xml': 'Idées',
    }
    
    stories_by_feed = {}
    
    # Parse each RSS feed and get first 3 titles
    for rss_url in rss_urls:
        try:
            feed = feedparser.parse(rss_url)
            
            if feed.bozo and feed.bozo_exception:
                stories_by_feed[rss_url] = {
                    'label': feed_labels.get(rss_url, 'Unknown'),
                    'titles': [],
                    'error': f"Error parsing feed: {feed.bozo_exception}"
                }
                continue
            
            if not feed.entries:
                stories_by_feed[rss_url] = {
                    'label': feed_labels.get(rss_url, 'Unknown'),
                    'titles': [],
                    'error': 'No entries found'
                }
                continue
            
            # Get first 3 titles
            titles = []
            for entry in feed.entries[:3]:
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                pub_date = None
                
                # Try to get publication date
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                    pub_date = timezone.make_aware(pub_date)
                
                if title:
                    titles.append({
                        'title': title,
                        'link': link,
                        'date': pub_date
                    })
            
            stories_by_feed[rss_url] = {
                'label': feed_labels.get(rss_url, 'Unknown'),
                'titles': titles,
                'error': None
            }
            
        except Exception as e:
            stories_by_feed[rss_url] = {
                'label': feed_labels.get(rss_url, 'Unknown'),
                'titles': [],
                'error': f"Error: {str(e)}"
            }
    
    # Optionally, save articles to database if requested
    if request.method == 'POST' and 'save_articles' in request.POST:
        try:
            # Use labels for each feed
            results = parse_rss_feeds(rss_urls)
            # Also save with individual labels
            for rss_url in rss_urls:
                label = feed_labels.get(rss_url, None)
                parse_rss_feeds([rss_url], label=label)
            
            messages.success(
                request, 
                f"Saved articles from {results['successful_feeds']} feeds."
            )
            return redirect('stories')
        except Exception as e:
            messages.error(request, f"Error saving articles: {str(e)}")
    
    context = {
        'stories_by_feed': stories_by_feed,
    }
    return render(request, 'main/stories.html', context)


@require_http_methods(["GET", "POST"])
def profile_settings(request):
    """View for editing user profile settings."""
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access profile settings.")
        return redirect('account_login')
    
    # Get or create user profile
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_settings')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileSettingsForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'main/profile_settings.html', context)
