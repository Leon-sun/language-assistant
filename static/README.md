# Static Files Directory

This directory contains static files for the Dictionary Project website.

## Directory Structure

```
static/
├── images/     # Place your images here (logos, banners, icons, etc.)
├── css/        # Custom CSS files
└── js/         # Custom JavaScript files
```

## How to Use Images in Templates

1. Place your image files in the `static/images/` folder
2. In your templates, use the `{% static %}` tag:

```django
{% load static %}

<!-- Example: Display an image -->
<img src="{% static 'images/logo.png' %}" alt="Logo">

<!-- Example: Background image -->
<div style="background-image: url('{% static 'images/banner.jpg' %}');">
    ...
</div>
```

## Supported Image Formats

- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.svg`
- `.webp`

## Collecting Static Files (for Production)

When deploying to production, run:

```bash
python manage.py collectstatic
```

This will collect all static files into a single directory for serving.
