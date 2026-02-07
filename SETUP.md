# Quick Setup Guide

## Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Set Gemini API Key

Create a `.env` file in the project root:

```bash
echo "GEMINI_API_KEY=your-actual-api-key-here" > .env
```

Or set it as an environment variable:

```bash
export GEMINI_API_KEY=your-actual-api-key-here
```

Get your API key from: https://makersuite.google.com/app/apikey

## Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 4: (Optional) Create Admin User

```bash
python manage.py createsuperuser
```

## Step 5: Start the Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Usage

1. Go to **Lookup Word** to translate French or English words
2. View the translation, explanations, and examples
3. Click **Save Word** to add it to your dictionary
4. Go to **Word List** to view and manage saved words
5. The prompt is configured in `dictionary_project/settings.py` (DICTIONARY_PROMPT)

## Troubleshooting

- **"GEMINI_API_KEY not found"**: Make sure you've set the API key in `.env` or as an environment variable
- **Database errors**: Run `python manage.py migrate` again
- **Import errors**: Make sure your virtual environment is activated
