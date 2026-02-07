"""
Service module for Gemini API integration.
"""
import os
import json
import re
import logging
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)


def get_gemini_client():
    """Initialize Gemini API client."""
    api_key = os.getenv('GEMINI_API_KEY') or getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in environment variables or settings.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-2.5-flash')


def build_personalized_prompt(word, user_profile=None):
    """
    Build a personalized prompt for word lookup based on user profile.
    
    Args:
        word: The word to lookup (str)
        user_profile: UserProfile instance or None
    
    Returns:
        tuple: (prompt_string, config_snapshot_dict)
    """
    # Safe attribute access with defaults
    if user_profile:
        age_group = getattr(user_profile, 'age_group', None) or 'adult'
        user_level = getattr(user_profile, 'level', None) or 'B1'
        learning_style = getattr(user_profile, 'learning_style', None) or 'Fun'
        target_language = getattr(user_profile, 'target_language', None) or 'fr'
        native_language = getattr(user_profile, 'native_language', None) or 'en'
        
        # Get top 3 interests from ManyToMany field
        try:
            user_interests_queryset = user_profile.interests.all()
            if user_interests_queryset.exists():
                # Get tag names, limit to 3
                top_interests = [tag.name for tag in user_interests_queryset[:3]]
            else:
                top_interests = ["General Knowledge", "Daily Life"]
        except Exception:
            top_interests = ["General Knowledge", "Daily Life"]
    else:
        age_group = 'adult'
        user_level = 'B1'
        learning_style = 'Fun'
        target_language = 'fr'
        native_language = 'en'
        top_interests = ["General Knowledge", "Daily Life"]
    
    interests_str = ", ".join(top_interests)
    
    # Determine tone based on learning style
    tone_instr = "Formal, precise, academic" if learning_style == 'Academic' else "Humorous, witty, engaging"
    
    # Language names mapping for better prompts
    language_names = {
        'fr': 'French',
        'en': 'English',
        'es': 'Spanish',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
    }
    target_lang_name = language_names.get(target_language, target_language.upper())
    native_lang_name = language_names.get(native_language, native_language.upper())
    
    prompt = f"""You are a highly personalized {target_lang_name} language tutor for a {age_group} student.
Level: {user_level}. Interests: [{interests_str}].

Target Word: "{word}"

**Instructions:**
1. **Context Selection (The Arbiter):** Select the ONE interest from [{interests_str}] that fits "{word}" most naturally. If none fit perfectly, choose the closest match.

2. **Content Generation:**
   - **Conversation (conversation_target):** Write 4-6 sentences in {target_lang_name} at {user_level} level, using the **selected interest** as the setting/context. Make it engaging and natural.
   - **Explanation (explanation_native):** Explain "{word}" using an analogy or example from the **selected interest** context. Write in {native_lang_name}, but make it relatable to the chosen interest.
   - **Examples (usages_target):** Provide exactly 3 different {target_lang_name} example sentences showing different usage contexts. Keep them at {user_level} level.
   - **Grammar Info:** Identify part_of_speech, base_form, and gender (if applicable for {target_lang_name}).

3. **Tone:** {tone_instr}

Return ONLY valid JSON. No markdown. No extra text.

Schema:
{{
  "input_word": "{word}",
  "target_language": "{target_language}",
  "native_language": "{native_language}",
  "selected_interest": "The chosen interest from the list",
  "part_of_speech": "verb" | "noun" | "adjective" | "adverb" | "other",
  "base_form": "string (infinitive for verbs, singular for nouns, masculine singular for adjectives)",
  "gender": "m" | "f" | null,
  "difficulty_system": "CEFR",
  "difficulty_level": "A1" | "A2" | "B1" | "B2" | "C1" | "C2",
  "conversation_target": "4-6 sentences in {target_lang_name} using the selected interest context",
  "explanation_native": "{native_lang_name} explanation using analogy from selected interest",
  "usages_target": ["sentence 1", "sentence 2", "sentence 3"]
}}
"""
    
    snapshot = {
        "target_age": age_group,
        "target_level": user_level,
        "target_language": target_language,
        "native_language": native_language,
        "candidate_interests": top_interests,
        "style": learning_style,
        "tone": tone_instr
    }
    
    return prompt, snapshot


def extract_json_from_text(text):
    """
    Robustly extract JSON from text that might contain markdown or extra text.
    
    Args:
        text: Text that may contain JSON
        
    Returns:
        str: Extracted JSON string
    """
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    
    # Try to find JSON object boundaries
    # Look for first { and last }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        text = text[start_idx:end_idx + 1]
    
    return text


def lookup_word(word, user_profile=None):
    """
    Lookup a word using Gemini API with personalized context-aware prompts.
    
    Args:
        word: The word to lookup (French or English)
        user_profile: UserProfile instance or None (for anonymous users)
    
    Returns:
        dict: Contains input_word, target_language, native_language, part_of_speech, base_form, gender, 
              difficulty_level (CEFR), selected_interest, conversation_target, explanation_native,
              usages_target (list of 3 items), and generation_config (snapshot).
              Also includes backward-compatible keys: conversation_fr, usages_fr, personalized_explanation,
              definition_en, cefr_level, language (when target_language='fr')
        
    Raises:
        ValueError: If API call fails or JSON parsing fails
    """
    try:
        model = get_gemini_client()
        
        # Build personalized prompt
        prompt, config_snapshot = build_personalized_prompt(word, user_profile)
        
        # Log prompt for debugging (only in DEBUG mode)
        if settings.DEBUG:
            logger.debug(f"Generated prompt for word '{word}':\n{prompt[:500]}...")
        
        # Generate content using Gemini with JSON response type
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,  # Lower temperature for more consistent JSON
                    "top_p": 0.8,
                    "top_k": 40,
                    "response_mime_type": "application/json",  # Request JSON directly
                }
            )
        except Exception as api_error:
            # Fallback if JSON mime type is not supported
            logger.warning(f"JSON mime type not supported, falling back to text: {str(api_error)}")
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "top_k": 40,
                }
            )
        
        # Extract the response content
        text = (response.text or "").strip()
        
        if settings.DEBUG:
            print("=== GEMINI RAW OUTPUT START ===")
            print(text)
            print("=== GEMINI RAW OUTPUT END ===")
        
        # Try direct JSON parsing first
        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            # Fallback to extract_json_from_text if direct parsing fails
            json_text = extract_json_from_text(text)
            
            # Try to fix common JSON issues
            json_text = re.sub(r',\s*}', '}', json_text)
            json_text = re.sub(r',\s*]', ']', json_text)
            
            try:
                result = json.loads(json_text)
            except json.JSONDecodeError as json_error:
                # Log the prompt for debugging
                logger.error(f"Failed to parse JSON. Prompt was: {prompt[:500]}...")
                logger.error(f"Response was: {text[:500]}...")
                raise ValueError(
                    f"Failed to parse JSON response. JSON Error: {str(json_error)}\n"
                    f"Response content: {text[:500]}"
                )
        
        # Inject generation config snapshot into result
        result['generation_config'] = config_snapshot
        
        # Extract language preferences from config or result
        target_language = result.get('target_language') or config_snapshot.get('target_language', 'fr')
        native_language = result.get('native_language') or config_snapshot.get('native_language', 'en')
        
        # Normalize language codes
        target_language = str(target_language).lower().strip()
        native_language = str(native_language).lower().strip()
        result['target_language'] = target_language
        result['native_language'] = native_language
        
        # Validate required fields (updated for new schema)
        # Accept both new schema keys and legacy keys for backward compatibility
        required_fields_new = [
            'input_word', 'target_language', 'native_language', 'part_of_speech', 'base_form', 
            'difficulty_level', 'selected_interest', 'conversation_target', 
            'explanation_native', 'usages_target'
        ]
        
        # Check if we have new schema or legacy schema
        has_new_schema = all(key in result for key in ['conversation_target', 'explanation_native', 'usages_target', 'difficulty_level'])
        has_legacy_schema = all(key in result for key in ['conversation_fr', 'personalized_explanation', 'usages_fr', 'cefr_level'])
        
        if not has_new_schema and not has_legacy_schema:
            missing_new = [f for f in required_fields_new if f not in result]
            missing_legacy = ['conversation_fr', 'personalized_explanation', 'usages_fr', 'cefr_level']
            raise ValueError(
                f"Missing required fields. Need either new schema ({', '.join(missing_new)}) "
                f"or legacy schema ({', '.join(missing_legacy)})\n"
                f"Response: {json.dumps(result, indent=2)}"
            )
        
        # Normalize to new schema format
        if has_legacy_schema and not has_new_schema:
            # Convert legacy to new format
            result['conversation_target'] = result.get('conversation_fr', '')
            result['explanation_native'] = result.get('personalized_explanation', '')
            result['usages_target'] = result.get('usages_fr', [])
            result['difficulty_level'] = result.get('cefr_level', 'B1')
            result['target_language'] = result.get('language', 'fr')
            if 'native_language' not in result:
                result['native_language'] = 'en'
        
        # Ensure we have the new schema keys
        result['conversation_target'] = str(result.get('conversation_target', '')).strip()
        result['explanation_native'] = str(result.get('explanation_native', '')).strip()
        result['usages_target'] = result.get('usages_target', [])
        result['difficulty_level'] = str(result.get('difficulty_level', '')).strip().upper()
        
        # Validate and normalize usages_target
        if not isinstance(result['usages_target'], list):
            raise ValueError(f"'usages_target' must be a list, got {type(result['usages_target'])}")
        
        usages = result['usages_target']
        if len(usages) != 3:
            # If we have more than 3, take first 3; if less, pad with empty strings
            if len(usages) > 3:
                usages = usages[:3]
            else:
                usages = usages + [''] * (3 - len(usages))
        result['usages_target'] = [str(u).strip() if u else '' for u in usages]
        
        # Ensure required fields are strings
        result['input_word'] = str(result.get('input_word', '')).strip()
        result['base_form'] = str(result.get('base_form', '')).strip()
        result['part_of_speech'] = str(result.get('part_of_speech', '')).strip()
        result['selected_interest'] = str(result.get('selected_interest', '')).strip()
        
        # Validate and normalize difficulty_level (CEFR)
        valid_cefr_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        if result['difficulty_level'] not in valid_cefr_levels:
            raise ValueError(f"Invalid difficulty_level: {result['difficulty_level']}. Must be one of: {', '.join(valid_cefr_levels)}")
        
        # Set cefr_level for backward compatibility
        result['cefr_level'] = result['difficulty_level']
        
        # Backward compatibility: Add legacy keys if target_language is French
        if target_language == 'fr':
            if 'conversation_fr' not in result:
                result['conversation_fr'] = result['conversation_target']
            if 'usages_fr' not in result:
                result['usages_fr'] = result['usages_target']
        
        # Backward compatibility: Always provide these legacy keys
        if 'personalized_explanation' not in result:
            result['personalized_explanation'] = result['explanation_native']
        if 'definition_en' not in result:
            result['definition_en'] = result['explanation_native']
        if 'language' not in result:
            result['language'] = target_language
        
        # Handle gender (can be null, "m", or "f")
        gender = result.get('gender')
        if gender is not None:
            result['gender'] = str(gender).strip().lower()
            if result['gender'] not in ['m', 'f']:
                result['gender'] = None
        else:
            result['gender'] = None
        
        return result
        
    except ValueError:
        # Re-raise ValueError as-is (these are our custom errors)
        raise
    except Exception as e:
        # Log the prompt if available for debugging
        if 'prompt' in locals():
            logger.error(f"Gemini API error with prompt: {prompt[:500]}...")
        logger.error(f"Gemini API error: {str(e)}")
        raise ValueError(f"Gemini API error: {str(e)}")


def generate_weather_phrase(temperature, weather_description, wind_speed=None):
    """
    Generate a fun and satirical phrase about the weather using Gemini (in French).
    
    Args:
        temperature: Current temperature in Celsius
        weather_description: Description of weather condition
        wind_speed: Wind speed in km/h (optional)
    
    Returns:
        str: Satirical weather phrase in French (max 30 words)
    """
    try:
        model = get_gemini_client()
        
        prompt = f"""Écris une phrase amusante et satirique sur la météo EN FRANÇAIS. 
        
Conditions actuelles:
- Température: {temperature}°C
- Météo: {weather_description}
{f'- Vitesse du vent: {wind_speed} km/h' if wind_speed else ''}

Exigences:
- Maximum 30 mots
- EN FRANÇAIS uniquement
- Sois humoristique et satirique
- Rends-la spirituelle et divertissante
- Garde un ton léger

Écris UNIQUEMENT la phrase, pas d'explications ni de texte supplémentaire."""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.8,  # Higher temperature for more creative responses
                "top_p": 0.9,
                "top_k": 40,
            }
        )
        
        phrase = (response.text or "").strip()
        
        # Limit to 30 words if Gemini exceeded
        words = phrase.split()
        if len(words) > 30:
            phrase = " ".join(words[:30]) + "..."
        
        return phrase
        
    except Exception as e:
        logger.error(f"Error generating weather phrase: {str(e)}")
        return f"Météo d'aujourd'hui: {weather_description} à {temperature}°C. Les sautes d'humeur de Mère Nature continuent!"


