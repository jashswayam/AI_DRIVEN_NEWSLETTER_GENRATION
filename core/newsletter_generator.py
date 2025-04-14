import datetime

class NewsletterGenerator:
    def __init__(self):
        self.now = datetime.datetime.now()
    
    def generate_newsletter(self, user_profile, articles, max_articles=10):
        """Generate a personalized newsletter in markdown format"""
        if not articles:
            return "No relevant articles found for your interests."
        
        # Get the top articles
        top_articles = articles[:max_articles]
        
        # Generate newsletter content
        newsletter = self._generate_header(user_profile)
        newsletter += self._generate_summary(top_articles[:3])
        newsletter += self._generate_sections(top_articles)
        
        return newsletter
    
    def _generate_header(self, user_profile):
        """Generate the newsletter header"""
        name = user_profile.get('name', 'Reader')
        date_str = self.now.strftime("%A, %B %d, %Y")
        
        header = f"# Personalized Newsletter for {name}\n\n"
        header += f"**{date_str}**\n\n"
        header += "---\n\n"
        
        return header
    
    def _generate_summary(self, top_articles):
        """Generate the top stories summary"""
        if not top_articles:
            return ""
            
        summary = "## Today's Top Stories\n\n"
        
        for article in top_articles:
            title = article.get('title', '')
            link = article.get('link', '')
            summary += f"- [{title}]({link})\n"
        
        summary += "\n---\n\n"
        return summary
    
    def _generate_sections(self, articles):
        """Generate sections by category"""
        # Group articles by category
        categories = {}
        for article in articles:
            category = article.get('category', 'General')
            if category not in categories:
                categories[category] = []
            categories[category].append(article)
        
        # Create sections for each category
        content = ""
        for category, category_articles in categories.items():
            content += f"## {category}\n\n"
            
            for article in category_articles[:3]:  # Limit to 3 articles per category
                title = article.get('title', '')
                link = article.get('link', '')
                summary = article.get('summary', '')
                source = article.get('source', '')
                
                # Clean and truncate summary
                summary = str(summary).replace('\n', ' ')
                if len(summary) > 200:
                    summary = summary[:197] + "..."
                
                content += f"### [{title}]({link})\n"
                content += f"**Source: {source}**\n\n"
                content += f"{summary}\n\n"
                content += f"[Read full article]({link})\n\n"
            
            content += "---\n\n"
        
        return content