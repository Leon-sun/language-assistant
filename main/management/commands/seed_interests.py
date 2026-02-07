"""
Management command to seed interest categories and tags.
Idempotent: can be run multiple times safely.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import InterestCategory, InterestTag


# Predefined taxonomy
TAXONOMY = {
    'Cooking & Food': [
        'French cuisine', 'Chinese cuisine', 'Cantonese cuisine',
        'Baking & desserts', 'Street food', 'Healthy cooking'
    ],
    'Movies & TV': [
        'French movies', 'Chinese movies', 'Hollywood movies',
        'TV series', 'Documentaries', 'Animation'
    ],
    'Reading & Literature': [
        'Novels', 'Short stories', 'Comics / Manga', 'Classic literature',
        'Modern fiction', 'Non-fiction'
    ],
    'Games & Entertainment': [
        'Video games', 'Board games', 'Mobile games', 'Puzzle games',
        'Role-playing games', 'Esports'
    ],
    'Culture & Society': [
        'French culture', 'Chinese culture', 'Traditions & festivals',
        'Daily life', 'History', 'Cross-cultural topics'
    ],
    'News & Current Affairs': [
        'World news', 'Technology news', 'Economy & business', 'Education',
        'Environment', 'Social issues'
    ],
    'Sports & Fitness': [
        'Hockey', 'Tennis', 'Swimming', 'Running', 'Skating', 'Fitness & training'
    ],
    'Travel & Geography': [
        'Travel stories', 'Cities & countries', 'Cultural travel', 'Food travel',
        'Nature & landscapes', 'Travel tips'
    ],
    'Music & Arts': [
        'Pop music', 'Classical music', 'Movie soundtracks', 'Painting & art',
        'Photography', 'Performing arts'
    ],
    'Language & Learning': [
        'French learning', 'Chinese learning', 'Vocabulary building',
        'Grammar practice', 'Speaking & pronunciation', 'Exam preparation'
    ],
}


class Command(BaseCommand):
    help = 'Seed interest categories and tags. Idempotent - safe to run multiple times.'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed interest categories and tags...')
        
        category_order = 0
        total_categories = 0
        total_tags = 0
        
        for category_name, tag_names in TAXONOMY.items():
            category_order += 1
            
            # Get or create category
            category, created = InterestCategory.objects.get_or_create(
                name=category_name,
                defaults={
                    'slug': slugify(category_name),
                    'order': category_order
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_name}')
                )
                total_categories += 1
            else:
                # Update order if it changed
                if category.order != category_order:
                    category.order = category_order
                    category.save()
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category_name}')
                )
            
            # Create tags for this category
            tag_order = 0
            for tag_name in tag_names:
                tag_order += 1
                
                tag, created = InterestTag.objects.get_or_create(
                    category=category,
                    name=tag_name,
                    defaults={
                        'slug': slugify(tag_name),
                        'order': tag_order
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'  Created tag: {tag_name}')
                    )
                    total_tags += 1
                else:
                    # Update order if it changed
                    if tag.order != tag_order:
                        tag.order = tag_order
                        tag.save()
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Seeding complete! '
                f'Categories: {total_categories} new, {len(TAXONOMY) - total_categories} existing. '
                f'Tags: {total_tags} new.'
            )
        )
