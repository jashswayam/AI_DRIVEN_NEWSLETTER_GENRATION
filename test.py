# test.py
from data.rss_feeds import get_rss_feeds
from data.user_profiles import get_user_profiles
from core.article_fetcher import ArticleFetcher
from core.content_analyzer import ContentAnalyzer
from core.personalization_engine import PersonalizationEngine
from core.newsletter_generator import NewsletterGenerator
from utils.config import get_content_categories
import sys
import os

def test_single_user():
    print("Starting newsletter generation test...")
    
    # Get test data
    rss_feeds = get_rss_feeds()
    user_profiles = get_user_profiles()
    categories = get_content_categories()
    
    # Choose a test feed and user
    test_feeds = []
    # Add some technology feeds - most relevant for Alex
    test_feeds.extend([
        "https://techcrunch.com/feed/",
        "https://www.wired.com/feed/rss"
    ])
    
    # Choose one user
    test_user_id = "alex"
    test_user = user_profiles[test_user_id]
    
    print(f"Testing with feeds: {test_feeds}")
    print(f"User profile: {test_user['name']}")
    print(f"Interests: {', '.join(test_user['interests'])}")
    print(f"Sources: {', '.join(test_user['sources'])}")
    
    # Initialize components
    fetcher = ArticleFetcher(test_feeds)
    analyzer = ContentAnalyzer()
    personalization = PersonalizationEngine(user_profiles)
    generator = NewsletterGenerator()
    
    # Fetch articles
    print("\nFetching articles...")
    all_articles = fetcher.fetch_articles(days_back=2)  # Last 2 days of articles
    
    if not all_articles:
        print("\nNo articles fetched. Using dummy data for testing...")
        # Create some dummy articles for testing when no real data is available
        all_articles = [
            {
                'title': 'New AI System Revolutionizes Medical Diagnostics',
                'summary': 'A team of researchers has developed a new AI system that can diagnose diseases with 95% accuracy, potentially transforming healthcare.',
                'link': 'https://example.com/ai-medical',
                'source': 'TechCrunch',
                'published': datetime.datetime.now(datetime.timezone.utc),
                'published_str': '2023-04-13T10:00:00Z'
            },
            {
                'title': 'Latest Cybersecurity Threats in 2023',
                'summary': 'Experts warn about new types of ransomware attacks targeting critical infrastructure and personal devices.',
                'link': 'https://example.com/cyber-threats',
                'source': 'Wired Tech',
                'published': datetime.datetime.now(datetime.timezone.utc),
                'published_str': '2023-04-14T09:15:00Z'
            },
            {
                'title': 'Blockchain Adoption in Financial Services',
                'summary': 'Major banks are increasingly implementing blockchain solutions for secure transactions and record keeping.',
                'link': 'https://example.com/blockchain-finance',
                'source': 'Ars Technica',
                'published': datetime.datetime.now(datetime.timezone.utc),
                'published_str': '2023-04-12T14:30:00Z'
            }
        ]
    
    print(f"\nProcessing {len(all_articles)} articles")
    
    # Process articles
    categorized_articles = {}
    
    for article in all_articles:
        # Extract keywords
        article_text = f"{article['title']} {article.get('summary', '')}"
        keywords = analyzer.extract_keywords(article_text)
        article['keywords'] = keywords
        print(f"\nArticle: {article['title']}")
        print(f"Keywords: {', '.join(keywords)}")
        
        # Determine category
        category = analyzer.categorize_article(article, categories)
        article['category'] = category
        print(f"Categorized as: {category}")
        
        if category not in categorized_articles:
            categorized_articles[category] = []
        
        categorized_articles[category].append(article)
    
    # Print categorization results
    print("\nCategorization Results:")
    for category, articles in categorized_articles.items():
        print(f"- {category}: {len(articles)} articles")
    
    # Filter for user
    user_articles = personalization.filter_articles_for_user(test_user_id, categorized_articles)
    print(f"\nFiltered {len(user_articles)} articles for {test_user['name']}")
    
    # Generate newsletter
    newsletter = generator.generate_newsletter(test_user, user_articles)
    
    # Print newsletter
    print("\n--- GENERATED NEWSLETTER ---\n")
    print(newsletter)
    
    # Save newsletter to file
    try:
        with open(f"{test_user_id}_test_newsletter.md", 'w', encoding='utf-8') as f:
            f.write(newsletter)
        print(f"\nNewsletter saved to {test_user_id}_test_newsletter.md")
    except Exception as e:
        print(f"Error saving newsletter: {str(e)}")

if __name__ == "__main__":
    try:
        # Ensure directories exist
        import os
        os.makedirs("data", exist_ok=True)
        os.makedirs("core", exist_ok=True)
        os.makedirs("utils", exist_ok=True)
        
        # Import missing modules
        import datetime
        
        # Check if module files exist, if not create them
        module_files = [
            "data/rss_feeds.py",
            "data/user_profiles.py",
            "utils/config.py"
        ]
        
        for file_path in module_files:
            if not os.path.exists(file_path):
                print(f"Creating module file: {file_path}")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    if file_path == "data/rss_feeds.py":
                        f.write("""
def get_rss_feeds():
    \"\"\"Return categorized RSS feeds\"\"\"
    return {
        "General News": [
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "http://feeds.reuters.com/reuters/topNews"
        ],
        "Technology": [
            "https://techcrunch.com/feed/",
            "https://www.wired.com/feed/rss",
            "https://www.technologyreview.com/feed/"
        ],
        "Finance": [
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://www.ft.com/rss/home"
        ],
        "Sports": [
            "https://www.espn.com/espn/rss/news",
            "http://feeds.bbci.co.uk/sport/rss.xml"
        ],
        "Entertainment": [
            "https://variety.com/feed/",
            "https://www.hollywoodreporter.com/feed/"
        ],
        "Science": [
            "https://www.nasa.gov/rss/dyn/breaking_news.rss",
            "https://www.sciencedaily.com/rss/all.xml",
            "https://arstechnica.com/science/feed/"
        ]
    }
""")
                    elif file_path == "data/user_profiles.py":
                        f.write("""
def get_user_profiles():
    \"\"\"Return predefined user profiles\"\"\"
    return {
        "alex": {
            "name": "Alex Parker",
            "age": 28,
            "location": "USA",
            "interests": ["AI", "cybersecurity", "blockchain", "startups", "programming"],
            "sources": ["TechCrunch", "Wired Tech", "Ars Technica", "MIT Tech Review"]
        },
        "priya": {
            "name": "Priya Sharma",
            "age": 35,
            "location": "India",
            "interests": ["Global markets", "startups", "fintech", "cryptocurrency", "economics"],
            "sources": ["Bloomberg", "Financial Times", "Forbes", "CoinDesk"]
        },
        "marco": {
            "name": "Marco Rossi",
            "age": 30,
            "location": "Italy",
            "interests": ["Football", "F1", "NBA", "Olympic sports", "esports"],
            "sources": ["ESPN", "BBC Sport", "Sky Sports F1", "The Athletic"]
        },
        "lisa": {
            "name": "Lisa Thompson",
            "age": 24,
            "location": "UK",
            "interests": ["Movies", "celebrity news", "TV shows", "music", "books"],
            "sources": ["Variety", "Rolling Stone", "Billboard", "Hollywood Reporter"]
        },
        "david": {
            "name": "David Martinez",
            "age": 40,
            "location": "Spain",
            "interests": ["Space exploration", "AI", "biotech", "physics", "renewable energy"],
            "sources": ["NASA", "Science Daily", "Nature", "Ars Technica Science"]
        }
    }
""")
                    elif file_path == "utils/config.py":
                        f.write("""
def get_content_categories():
    \"\"\"Return category definitions with keywords\"\"\"
    return {
        "Technology": [
            "technology", "tech", "AI", "artificial intelligence", "machine learning",
            "programming", "software", "hardware", "app", "smartphone", "computer",
            "algorithm", "code", "developer", "engineering", "cybersecurity", "blockchain"
        ],
        "Finance": [
            "finance", "economy", "stock", "market", "banking", "investment", "currency",
            "economics", "financial", "business", "trade", "money", "crypto", "bitcoin",
            "fintech", "loan", "capital", "economic"
        ],
        "Sports": [
            "sport", "football", "soccer", "basketball", "baseball", "tennis",
            "athlete", "championship", "tournament", "match", "game", "racing",
            "team", "player", "league", "NFL", "NBA", "FIFA", "Olympics", "esports"
        ],
        "Entertainment": [
            "entertainment", "movie", "film", "music", "celebrity", "actor", "actress",
            "hollywood", "TV", "television", "show", "star", "director", "artist",
            "concert", "album", "release", "netflix", "streaming", "book", "author"
        ],
        "Science": [
            "science", "scientific", "research", "study", "experiment", "laboratory",
            "discovery", "physics", "chemistry", "biology", "astronomy", "space",
            "planet", "universe", "NASA", "molecule", "theory", "medical", "health",
            "energy", "renewable", "climate", "environment", "biotech"
        ],
        "Politics": [
            "politics", "political", "government", "election", "president", "minister",
            "policy", "vote", "democracy", "republic", "parliament", "campaign",
            "party", "senator", "congress", "law", "legislation", "international",
            "diplomatic", "relations", "leader", "nation", "country"
        ]
    }
""")
        
        # Now run the test
        test_single_user()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()