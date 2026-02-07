# Dictionary Project - Django Web Application

A French-English dictionary web application powered by Django and Google Gemini AI. Lookup words, get translations, explanations, and usage examples, then save them to your personal word list.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Gemini API key (get one from https://makersuite.google.com/app/apikey)

## Setup Instructions

### 1. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Gemini API Key

Create a `.env` file in the project root (or set environment variable):

```bash
# Option 1: Create .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env

# Option 2: Set environment variable
export GEMINI_API_KEY=your-api-key-here
```

**Note:** The application will look for `GEMINI_API_KEY` in environment variables. You can also set it directly in `dictionary_project/settings.py` (not recommended for production).

### 4. Run Database Migrations

```bash
python manage.py migrate
```

This will create the SQLite database and set up the necessary tables.

### 5. Create a Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
Dictionary Project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── dictionary_project/       # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── main/                    # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Word model
│   ├── views.py             # Dictionary views
│   ├── forms.py             # Forms for word lookup
│   ├── services.py          # OpenAI API integration
│   └── urls.py
├── templates/               # HTML templates
│   ├── base.html
│   └── main/
│       ├── index.html
│       └── about.html
└── static/                  # Static files (CSS, JS, images)
```

## Available URLs

- `/` - Home page
- `/lookup/` - Word lookup and translation
- `/words/` - List of saved words
- `/words/<id>/` - Word detail page
- `/words/<id>/delete/` - Delete word
- `/about/` - About page
- `/admin/` - Django admin panel (requires superuser)

## Features

1. **Word Lookup**: Enter French or English words to get:
   - French word in basic form
   - English translation and explanation
   - French explanation
   - 3 usage examples in English
   - 3 usage examples in French

2. **Word Management**: 
   - Save words to your personal dictionary
   - Filter words by difficulty level (Beginner, Intermediate, Advanced)
   - Track familiarity (New, Learning, Familiar, Mastered)
   - Edit word metadata
   - Delete words

3. **Gemini AI Integration**:
   - Powered by Google Gemini AI for accurate translations
   - Prompt configured in settings (not visible on webpage)
   - Uses Gemini Pro model for translations

## Word Model

The `Word` model includes:
- `original_word`: The word entered by user
- `french_word`: French word in basic form
- `english_translation`: English explanation
- `french_explanation`: French explanation
- `english_examples`: 3 English usage examples
- `french_examples`: 3 French usage examples
- `difficulty_level`: Beginner, Intermediate, or Advanced
- `familiarity`: New, Learning, Familiar, or Mastered
- `openai_prompt`: The prompt used for translation (for reference, stored in database)
- `created_at` and `updated_at`: Timestamps

## Development Tips

- The project uses SQLite by default (good for development)
- Debug mode is enabled (change `DEBUG = False` in production)
- Static files are configured for development
- Templates use Django's template language

## Troubleshooting

- **Import errors**: Make sure your virtual environment is activated
- **Database errors**: Run `python manage.py migrate` again
- **Port already in use**: Use `python manage.py runserver 8001` to use a different port
- **Gemini API errors**: 
  - Make sure `GEMINI_API_KEY` is set correctly
  - Check your Google Cloud account has API access enabled
  - Verify the API key has proper permissions
- **Word lookup fails**: The prompt is configured in `dictionary_project/settings.py` (DICTIONARY_PROMPT)

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
