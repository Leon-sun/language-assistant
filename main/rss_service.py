"""
Service module for RSS feed parsing and article management.
"""
import feedparser
from datetime import datetime
from django.utils import timezone
from .models import Article
import logging

logger = logging.getLogger(__name__)


def parse_rss_feeds(rss_urls, label=None):
    """
    Parse multiple RSS feeds and save articles to the database.
    
    Args:
        rss_urls: List of RSS feed URLs to parse
        label: Optional label to assign to all articles from these feeds
    
    Returns:
        dict: Summary of parsing results with counts and errors
    """
    results = {
        'total_feeds': len(rss_urls),
        'successful_feeds': 0,
        'failed_feeds': 0,
        'articles_created': 0,
        'articles_skipped': 0,
        'errors': []
    }
    
    for rss_url in rss_urls:
        try:
            # Parse the RSS feed
            feed = feedparser.parse(rss_url)
            
            if feed.bozo and feed.bozo_exception:
                error_msg = f"Error parsing RSS feed {rss_url}: {feed.bozo_exception}"
                logger.warning(error_msg)
                results['errors'].append(error_msg)
                results['failed_feeds'] += 1
                continue
            
            if not feed.entries:
                logger.warning(f"No entries found in RSS feed: {rss_url}")
                results['failed_feeds'] += 1
                continue
            
            # Process each entry in the feed
            for entry in feed.entries:
                try:
                    # Extract title
                    title = entry.get('title', '').strip()
                    if not title:
                        logger.warning(f"Skipping entry with no title from {rss_url}")
                        results['articles_skipped'] += 1
                        continue
                    
                    # Extract content
                    content = ''
                    if hasattr(entry, 'content') and entry.content:
                        # Some feeds have content as a list
                        if isinstance(entry.content, list) and len(entry.content) > 0:
                            content = entry.content[0].get('value', '')
                        else:
                            content = str(entry.content)
                    elif hasattr(entry, 'summary'):
                        content = entry.summary
                    elif hasattr(entry, 'description'):
                        content = entry.description
                    
                    # Extract date
                    article_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        article_date = datetime(*entry.published_parsed[:6])
                        article_date = timezone.make_aware(article_date)
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        article_date = datetime(*entry.updated_parsed[:6])
                        article_date = timezone.make_aware(article_date)
                    else:
                        # Use current time if no date available
                        article_date = timezone.now()
                    
                    # Extract source URL
                    source_url = entry.get('link', '')
                    
                    # Check if article already exists (by title and date to avoid duplicates)
                    existing = Article.objects.filter(
                        title=title,
                        date=article_date
                    ).first()
                    
                    if existing:
                        logger.debug(f"Article already exists: {title}")
                        results['articles_skipped'] += 1
                        continue
                    
                    # Create article
                    article = Article.objects.create(
                        title=title,
                        content=content,
                        date=article_date,
                        label=label,
                        source_url=source_url,
                        rss_feed_url=rss_url,
                    )
                    
                    results['articles_created'] += 1
                    logger.info(f"Created article: {title}")
                    
                except Exception as e:
                    error_msg = f"Error processing entry from {rss_url}: {str(e)}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['articles_skipped'] += 1
                    continue
            
            results['successful_feeds'] += 1
            
        except Exception as e:
            error_msg = f"Error parsing RSS feed {rss_url}: {str(e)}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            results['failed_feeds'] += 1
            continue
    
    return results


def parse_single_rss_feed(rss_url, label=None):
    """
    Parse a single RSS feed and save articles.
    
    Args:
        rss_url: Single RSS feed URL
        label: Optional label to assign to articles
    
    Returns:
        dict: Parsing results
    """
    return parse_rss_feeds([rss_url], label=label)
