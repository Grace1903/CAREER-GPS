"""
Helper Functions
"""
import re
import json


def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s\.\,\-\@\#\+]', '', text)
    
    return text.strip()


def calculate_similarity(list1, list2):
    """Calculate Jaccard similarity between two lists"""
    if not list1 or not list2:
        return 0.0
    
    set1 = set([s.lower() for s in list1])
    set2 = set([s.lower() for s in list2])
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0


def load_json_file(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}


def format_duration(hours):
    """Format duration in hours to human readable"""
    if hours < 1:
        return f"{int(hours * 60)} minutes"
    elif hours < 24:
        return f"{hours} hours"
    elif hours < 168:  # 7 days
        days = hours / 24
        return f"{days:.1f} days"
    else:
        weeks = hours / 168
        return f"{weeks:.1f} weeks"