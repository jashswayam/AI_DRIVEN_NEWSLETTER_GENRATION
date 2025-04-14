# core/personalization_engine.py
class PersonalizationEngine:
    def __init__(self, user_profiles):
        self.user_profiles = user_profiles
    
    def get_user_profile(self, user_id):
        """Retrieve user profile by ID"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        return None
    
    def filter_articles_for_user(self, user_id, categorized_articles):
        """Filter articles based on user preferences"""
        user_profile = self.get_user_profile(user_id)
        if not user_profile:
            return []
        
        # Extract user interests and preferred sources
        interests = [interest.lower() for interest in user_profile.get('interests', [])]
        preferred_sources = user_profile.get('sources', [])
        
        filtered_articles = []
        
        # Check each category of articles
        for category, articles in categorized_articles.items():
            # Is this category related to user interests?
            category_relevant = False
            
            # Check if category name matches any interest
            if any(interest in category.lower() for interest in interests):
                category_relevant = True
            
            # Check for each article
            for article in articles:
                article_added = False
                source = article.get('source', '')
                
                # Check if source matches preferred sources
                source_match = any(s.lower() in source.lower() for s in preferred_sources)
                
                # Check if keywords match user interests
                keywords = article.get('keywords', [])
                keyword_match = any(interest in ' '.join(keywords).lower() for interest in interests)
                
                # Decision logic for including article
                if category_relevant or keyword_match:
                    # Assign relevance score
                    if source_match:
                        article['relevance_score'] = 2  # High relevance: matches both interest and source
                    else:
                        article['relevance_score'] = 1  # Medium relevance: matches interest only
                        
                    filtered_articles.append(article)
                    article_added = True
                elif source_match:
                    # Include if source matches, even if category doesn't
                    article['relevance_score'] = 1  # Medium relevance: matches source only
                    filtered_articles.append(article)
                    article_added = True
                    
                if article_added:
                    print(f"Added relevant article for {user_id}: {article['title']} (Score: {article.get('relevance_score', 0)})")
        
        # Sort by relevance score and then by published date
        filtered_articles.sort(key=lambda x: (x.get('relevance_score', 0)), reverse=True)
        
        return filtered_articles