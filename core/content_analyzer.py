from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import re

class ContentAnalyzer:
    def __init__(self):
        # Download necessary NLTK data
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            text = str(text)
            
        # Convert to lowercase
        text = text.lower()
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_keywords(self, text, top_n=5):
        """Extract key terms from text"""
        processed_text = self.preprocess_text(text)
        
        # Tokenize
        words = processed_text.split()
        
        # Remove stop words
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Return top N keywords
        return [word for word, freq in sorted_words[:top_n]] if sorted_words else ["general"]
    
    def categorize_article(self, article, categories):
        """Categorize an article based on predefined categories"""
        article_text = f"{article['title']} {article.get('summary', '')}"
        article_text = self.preprocess_text(article_text)
        
        best_match = "General"  # Default category
        highest_score = 0.1  # Threshold for matching
        
        for category, keywords in categories.items():
            # Calculate similarity between article and category keywords
            score = self._calculate_similarity(article_text, " ".join(keywords))
            
            if score > highest_score:
                highest_score = score
                best_match = category
        
        return best_match
    
    def _calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        try:
            # If either text is too short, similarity calculation may be unreliable
            if len(text1) < 10 or len(text2) < 10:
                return 0
                
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0
