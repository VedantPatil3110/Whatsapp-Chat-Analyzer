import re
import emoji
from collections import Counter
import pandas as pd

def get_top_words(df, n=10):
    """
    Extract the most frequently used words in the chat.
    
    Args:
        df (pd.DataFrame): DataFrame with messages
        n (int): Number of top words to return
    
    Returns:
        list: List of dictionaries with word and count
    """
    # Common stop words to filter out
    stop_words = {
        'the', 'and', 'is', 'in', 'it', 'to', 'of', 'for', 'with', 'on',
        'that', 'this', 'was', 'at', 'from', 'by', 'as', 'an', 'are', 'be',
        'been', 'being', 'if', 'into', 'not', 'such', 'no', 'nor', 'too',
        'very', 'can', 'just', 'should', 'now'
    }
    
    # Combine all messages
    all_text = ' '.join(df['message'].tolist())
    
    # Remove emojis and URLs
    all_text = emoji.replace_emoji(all_text, '')
    all_text = re.sub(r'http\S+', '', all_text)
    
    # Tokenize and filter words
    words = re.findall(r'\b[a-zA-Z]{3,15}\b', all_text.lower())
    words = [word for word in words if word not in stop_words]
    
    # Count frequencies
    word_counts = Counter(words)
    
    # Get top N words
    top_words = [{"word": word, "count": count} 
                 for word, count in word_counts.most_common(n)]
    
    return top_words

def get_top_emojis(df, n=10):
    """
    Extract the most frequently used emojis in the chat.
    
    Args:
        df (pd.DataFrame): DataFrame with messages
        n (int): Number of top emojis to return
    
    Returns:
        list: List of dictionaries with emoji and count
    """
    # Combine all messages
    all_text = ' '.join(df['message'].tolist())
    
    # Extract emojis
    emojis = [c for c in all_text if c in emoji.EMOJI_DATA]
    
    # Count frequencies
    emoji_counts = Counter(emojis)
    
    # Get top N emojis
    top_emojis = [{"emoji": emoji, "count": count} 
                  for emoji, count in emoji_counts.most_common(n)]
    
    return top_emojis

def get_hourly_activity(df):
    """
    Extract message activity by hour of day.
    
    Args:
        df (pd.DataFrame): DataFrame with messages
    
    Returns:
        list: List of dictionaries with hour and count
    """
    # Create a full range of hours (0-23)
    all_hours = pd.DataFrame({'hour': range(24)})
    
    # Group by hour and count messages
    hourly_counts = df.groupby('hour').size().reset_index()
    hourly_counts.columns = ['hour', 'count']
    
    # Merge with all_hours to include all hours
    hourly_counts = all_hours.merge(hourly_counts, on='hour', how='left')
    hourly_counts['count'] = hourly_counts['count'].fillna(0).astype(int)
    
    # Convert to list of dictionaries
    hourly_activity = hourly_counts.to_dict('records')
    
    return hourly_activity