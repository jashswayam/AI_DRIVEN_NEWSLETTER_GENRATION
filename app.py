import streamlit as st
import datetime
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent))

# Import our newsletter components
from data.rss_feeds import get_rss_feeds
from data.user_profiles import get_user_profiles
from core.article_fetcher import ArticleFetcher
from core.content_analyzer import ContentAnalyzer
from core.personalization_engine import PersonalizationEngine
from core.newsletter_generator import NewsletterGenerator
from utils.config import get_content_categories

# Configure the page
st.set_page_config(
    page_title="AI Personalized Newsletter",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("📰 AI-Powered Personalized Newsletter")
st.markdown("Generate personalized newsletters based on your interests and preferences")

# Create a sidebar for controls
st.sidebar.header("Settings")

# Get user profiles and show selection dropdown
user_profiles = get_user_profiles()
user_names = {user_id: profile["name"] for user_id, profile in user_profiles.items()}
selected_user = st.sidebar.selectbox("Select User", list(user_names.keys()), format_func=lambda x: user_names[x])

# Display selected user profile
selected_profile = user_profiles[selected_user]
st.sidebar.subheader("User Profile")
st.sidebar.write(f"**Name:** {selected_profile['name']}")
st.sidebar.write(f"**Age:** {selected_profile['age']}")
st.sidebar.write(f"**Location:** {selected_profile['location']}")
st.sidebar.write(f"**Interests:** {', '.join(selected_profile['interests'])}")
st.sidebar.write(f"**Preferred Sources:** {', '.join(selected_profile['sources'])}")

# Options for newsletter generation
st.sidebar.subheader("Newsletter Options")
days_back = st.sidebar.slider("Include articles from past days:", 1, 7, 2)
max_articles = st.sidebar.slider("Maximum articles per newsletter:", 5, 20, 10)
email_address = st.sidebar.text_input("Email address for delivery (optional):")

# Function to generate newsletter
def generate_newsletter():
    with st.spinner("Fetching and analyzing articles..."):
        progress_bar = st.progress(0)
        
        # Get RSS feeds
        rss_feeds = get_rss_feeds()
        categories = get_content_categories()
        
        # Flatten the RSS feeds for the fetcher
        all_feeds = []
        for category_feeds in rss_feeds.values():
            all_feeds.extend(category_feeds)
        
        progress_bar.progress(10)
        
        # Initialize components
        fetcher = ArticleFetcher(all_feeds)
        analyzer = ContentAnalyzer()
        personalization = PersonalizationEngine(user_profiles)
        generator = NewsletterGenerator()
        
        progress_bar.progress(20)
        
        # Fetch articles
        st.info(f"Fetching articles from {len(all_feeds)} feeds...")
        all_articles = fetcher.fetch_articles(days_back=days_back)
        
        progress_bar.progress(50)
        
        if not all_articles:
            st.warning("No articles found. Using sample data for testing.")
            # Create sample articles for demonstration
            all_articles = [
                {
                    'title': 'New AI System Revolutionizes Medical Diagnostics',
                    'summary': 'A team of researchers has developed a new AI system that can diagnose diseases with 95% accuracy, potentially transforming healthcare.',
                    'link': 'https://example.com/ai-medical',
                    'source': 'TechCrunch',
                    'published': datetime.datetime.now(),
                    'category': 'Technology'
                },
                {
                    'title': 'SpaceX Launches New Satellite Constellation',
                    'summary': 'SpaceX successfully launched 60 new satellites into orbit, expanding their network for global internet coverage.',
                    'link': 'https://example.com/spacex-launch',
                    'source': 'NASA',
                    'published': datetime.datetime.now() - datetime.timedelta(days=1),
                    'category': 'Science'
                },
                {
                    'title': 'Major Security Vulnerability Found in Popular Software',
                    'summary': 'Cybersecurity researchers have discovered a critical vulnerability affecting millions of devices. Patches are being developed.',
                    'link': 'https://example.com/security-news',
                    'source': 'Ars Technica',
                    'published': datetime.datetime.now() - datetime.timedelta(hours=12),
                    'category': 'Technology'
                },
                {
                    'title': 'New Programming Language Gains Popularity Among Developers',
                    'summary': 'A new programming language designed for AI applications is seeing rapid adoption in the developer community.',
                    'link': 'https://example.com/new-language',
                    'source': 'MIT Tech Review',
                    'published': datetime.datetime.now() - datetime.timedelta(days=2),
                    'category': 'Technology'
                },
                {
                    'title': 'Blockchain Technology Transforms Supply Chain Management',
                    'summary': 'Companies are increasingly adopting blockchain solutions to improve transparency and efficiency in their supply chains.',
                    'link': 'https://example.com/blockchain-supply',
                    'source': 'TechCrunch',
                    'published': datetime.datetime.now() - datetime.timedelta(hours=36),
                    'category': 'Technology'
                }
            ]
        
        st.info(f"Categorizing {len(all_articles)} articles...")
        progress_bar.progress(60)
        
        # Categorize articles
        categorized_articles = {}
        for article in all_articles:
            # Skip categorization if already categorized (from sample data)
            if 'category' not in article:
                # Extract keywords from article
                keywords = analyzer.extract_keywords(f"{article['title']} {article['summary']}")
                article['keywords'] = keywords
                
                # Determine category
                category = analyzer.categorize_article(article, categories)
                article['category'] = category
            
            category = article['category']
            if category not in categorized_articles:
                categorized_articles[category] = []
            
            categorized_articles[category].append(article)
        
        progress_bar.progress(80)
        
        # Filter articles for this user
        user_articles = personalization.filter_articles_for_user(selected_user, categorized_articles)
        
        # Generate newsletter
        newsletter = generator.generate_newsletter(selected_profile, user_articles, max_articles)
        
        progress_bar.progress(100)
        
        return newsletter, user_articles

# Generate button
if st.sidebar.button("Generate Newsletter"):
    newsletter_content, user_articles = generate_newsletter()
    
    # Store in session state
    st.session_state.newsletter_content = newsletter_content
    st.session_state.user_articles = user_articles
    st.session_state.generated = True
    
    # Save to file (optional)
    newsletter_file = f"{selected_user}_newsletter.md"
    with open(newsletter_file, "w") as f:
        f.write(newsletter_content)

# Email delivery button (simulation)
if st.sidebar.button("Deliver Newsletter") and email_address:
    st.sidebar.success(f"Newsletter would be delivered to {email_address} in a real implementation")
    st.balloons()

# Display newsletter if generated
if 'generated' in st.session_state and st.session_state.generated:
    st.subheader("Your Personalized Newsletter")
    
    # Display article stats
    if 'user_articles' in st.session_state:
        articles = st.session_state.user_articles
        col1, col2, col3 = st.columns(3)
        col1.metric("Articles Found", len(articles))
        
        # Count articles by source
        sources = {}
        for article in articles:
            source = article.get('source', 'Unknown')
            if source in sources:
                sources[source] += 1
            else:
                sources[source] = 1
        
        top_source = max(sources.items(), key=lambda x: x[1])[0] if sources else "None"
        col2.metric("Top Source", top_source)
        
        # Count articles by category
        categories = {}
        for article in articles:
            category = article.get('category', 'Unknown')
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
        
        top_category = max(categories.items(), key=lambda x: x[1])[0] if categories else "None"
        col3.metric("Top Category", top_category)
    
    # Display tabs for different views
    tab1, tab2 = st.tabs(["Rendered View", "Markdown Source"])
    
    with tab1:
        st.markdown(st.session_state.newsletter_content)
    
    with tab2:
        st.code(st.session_state.newsletter_content, language="markdown")
    
    # Download button
    st.download_button(
        label="Download Newsletter",
        data=st.session_state.newsletter_content,
        file_name=f"{selected_user}_newsletter_{datetime.datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
    )

# Add some usage instructions if newsletter not yet generated
else:
    st.info("Select a user from the sidebar and click 'Generate Newsletter' to create a personalized newsletter.")
    
    # Show example of what will be generated
    with st.expander("See example newsletter"):
        st.markdown("""
        # Personalized Newsletter for Example User
        
        **Monday, April 14, 2025**
        
        ---
        
        ## Today's Top Stories
        
        - [New AI System Revolutionizes Medical Diagnostics](https://example.com/ai-medical)
        - [SpaceX Launches New Satellite Constellation](https://example.com/spacex-launch)
        - [Major Security Vulnerability Found in Popular Software](https://example.com/security-news)
        
        ---
        
        ## Technology
        
        ### [New AI System Revolutionizes Medical Diagnostics](https://example.com/ai-medical)
        **Source: TechCrunch**
        
        A team of researchers has developed a new AI system that can diagnose diseases with 95% accuracy, potentially transforming healthcare.
        
        [Read full article](https://example.com/ai-medical)
        
        ### [Major Security Vulnerability Found in Popular Software](https://example.com/security-news)
        **Source: Ars Technica**
        
        Cybersecurity researchers have discovered a critical vulnerability affecting millions of devices. Patches are being developed.
        
        [Read full article](https://example.com/security-news)
        
        ---
        
        ## Science
        
        ### [SpaceX Launches New Satellite Constellation](https://example.com/spacex-launch)
        **Source: NASA**
        
        SpaceX successfully launched 60 new satellites into orbit, expanding their network for global internet coverage.
        
        [Read full article](https://example.com/spacex-launch)
        
        ---
        """)

# Add footer with attribution
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and AI")
