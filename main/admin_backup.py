from django.contrib import admin
from .models import (
    Word, UserProfile, Article, GlobalWord, ContentCard, UserVocabulary,
    InterestCategory, InterestTag
)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['french_word', 'original_word', 'cefr_level', 'familiarity', 'created_at']
    list_filter = ['cefr_level', 'familiarity', 'created_at']
    search_fields = ['french_word', 'original_word', 'english_translation']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(InterestCategory)
class InterestCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'slug']
    readonly_fields = ['created_at']
    ordering = ['order', 'name']


@admin.register(InterestTag)
class InterestTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'order', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'slug', 'category__name']
    readonly_fields = ['created_at']
    ordering = ['category__order', 'category__name', 'order', 'name']
    autocomplete_fields = ['category']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'level', 'contact', 'created_at']
    list_filter = ['level', 'interests', 'created_at']
    search_fields = ['user__username', 'user__email', 'nickname', 'contact']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['interests']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'nickname')
        }),
        ('Profile Details', {
            'fields': ('level', 'interests', 'learning_goals', 'contact')
        }),
        ('Deprecated Fields', {
            'fields': ('interest',),
            'classes': ('collapse',),
            'description': 'Old interest field kept for migration. Use interests (tags) instead.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'label', 'date', 'rss_feed_url', 'created_at']
    list_filter = ['label', 'date', 'created_at']
    search_fields = ['title', 'content', 'label', 'source_url']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'content', 'label')
        }),
        ('Source Information', {
            'fields': ('source_url', 'rss_feed_url', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GlobalWord)
class GlobalWordAdmin(admin.ModelAdmin):
    list_display = ['text', 'language', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ContentCard)
class ContentCardAdmin(admin.ModelAdmin):
    list_display = ['word', 'target_cefr', 'interest_context', 'tone_style', 'created_at']
    list_filter = ['target_cefr', 'interest_context', 'tone_style', 'created_at']
    search_fields = ['word__text', 'definition']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Word Reference', {
            'fields': ('word',)
        }),
        ('Content', {
            'fields': ('definition', 'conversation', 'examples')
        }),
        ('Meta-Tags (Reuse Index)', {
            'fields': ('target_cefr', 'interest_context', 'tone_style')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserVocabulary)
class UserVocabularyAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'familiarity', 'added_at']
    list_filter = ['familiarity', 'added_at']
    search_fields = ['user__username', 'user__email', 'card__word__text']
    readonly_fields = ['added_at', 'updated_at']
