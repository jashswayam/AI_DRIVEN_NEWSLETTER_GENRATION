import feedparser
import datetime
from dateutil import parser as date_parser

class ArticleFetcher:
    def __init__(self, feed_urls):
        self.feed_urls = feed_urls
        
    def fetch_articles(self, days_back=1):
        """Fetch articles from RSS feeds"""
        all_articles = []
        current_time = datetime.datetime.now(datetime.timezone.utc)  # Make timezone-aware
        cutoff_time = current_time - datetime.timedelta(days=days_back)
        
        for feed_url in self.feed_urls:
            try:
                print(f"Fetching from {feed_url}...")
                feed = feedparser.parse(feed_url)
                source = feed.feed.get('title', 'Unknown Source')
                
                for entry in feed.entries:
                    # Try to extract the published date - different feeds use different fields
                    published_str = entry.get('published', entry.get('pubDate', entry.get('updated', '')))
                    
                    try:
                        # Use dateutil parser which handles many date formats
                        published = date_parser.parse(published_str)
                        
                        # Make naive datetime timezone-aware if it isn't already
                        if published.tzinfo is None:
                            published = published.replace(tzinfo=datetime.timezone.utc)
                            
                    except (AttributeError, ValueError):
                        # If parsing fails, use current time and mark it
                        published = current_time
                        published_str = "Unknown"
                    
                    # Only include recent articles
                    if published >= cutoff_time:
                        # Extract text summary, handle different formats
                        if 'summary' in entry:
                            summary = entry.summary
                        elif 'description' in entry:
                            summary = entry.description
                        else:
                            summary = ""
                            
                        article = {
                            'title': entry.get('title', 'Untitled'),
                            'link': entry.get('link', ''),
                            'summary': summary,
                            'published': published,
                            'published_str': published_str,
                            'source': source
                        }
                        all_articles.append(article)
                        print(f"Added article: {article['title']}")
            except Exception as e:
                print(f"Error fetching from {feed_url}: {str(e)}")
                
        print(f"Total articles fetched: {len(all_articles)}")
        return all_articles