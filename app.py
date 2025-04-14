# main.py
from data.rss_feeds import get_rss_feeds
from data.user_profiles import get_user_profiles
from core.article_fetcher import ArticleFetcher
from core.content_analyzer import ContentAnalyzer
from core.personalization_engine import PersonalizationEngine
from core.newsletter_generator import NewsletterGenerator
from utils.config import get_content_categories
import os

def main():
    # Initialize data
    rss_feeds = get_rss_feeds()
    user_profiles = get_user_profiles()
    categories = get_content_categories()
    
    # Create directories if they don't exist
    os.makedirs("newsletters", exist_ok=True)
    
    # Flatten the RSS feeds for the fetcher
    all_feeds = []
    for category_feeds in rss_feeds.values():
        all_feeds.extend(category_feeds)
    
    # Initialize components
    fetcher = ArticleFetcher(all_feeds)
    analyzer = ContentAnalyzer()
    personalization = PersonalizationEngine(user_profiles)
    generator = NewsletterGenerator()
    
    # Fetch articles
    print("Fetching articles...")
    all_articles = fetcher.fetch_articles(days_back=2)
    print(f"Fetched {len(all_articles)} articles")
    
    # Categorize articles
    print("Categorizing articles...")
    categorized_articles = {}
    for article in all_articles:
        # Extract keywords from article
        keywords = analyzer.extract_keywords(f"{article['title']} {article['summary']}")
        article['keywords'] = keywords
        
        # Determine category
        category = analyzer.categorize_article(article, categories)
        article['category'] = category
        
        if category not in categorized_articles:
            categorized_articles[category] = []
        
        categorized_articles[category].append(article)
    
    # Generate personalized newsletters for each user
    for user_id, profile in user_profiles.items():
        print(f"Generating newsletter for {profile['name']}...")
        
        # Filter articles for this user
        user_articles = personalization.filter_articles_for_user(user_id, categorized_articles)
        
        # Generate newsletter
        newsletter = generator.generate_newsletter(profile, user_articles)
        
        # Save newsletter to file
        file_name = f"newsletters/{user_id}_newsletter.md"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(newsletter)
        
        print(f"Newsletter saved to {file_name}")

if __name__ == "__main__":
    main()