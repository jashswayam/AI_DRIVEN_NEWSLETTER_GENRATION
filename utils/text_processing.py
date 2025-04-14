# text_processing.py
import re
from html import unescape

def clean_html(text):
    """Remove HTML tags from text"""
    # Remove HTML tags
    clean_text = re.sub(r'<.*?>', '', text)
    # Decode HTML entities
    clean_text = unescape(clean_text)
    return clean_text

def truncate_text(text, max_length=200):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at the end of a sentence within the last 20% of max_length
    truncate_range = int(max_length * 0.2)
    min_index = max_length - truncate_range
    max_index = max_length
    
    # Look for sentence endings (., !, ?) within the range
    for i in range(max_index, min_index, -1):
        if i < len(text) and text[i] in ['.', '!', '?']:
            return text[:i+1] + "..."
    
    # If no sentence ending found, just truncate at max_length
    return text[:max_length] + "..."