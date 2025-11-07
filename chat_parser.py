import re
import pandas as pd
import emoji
from datetime import datetime

def parse_whatsapp_chat(file_path):
    """
    Parse a WhatsApp chat export file and convert it to a pandas DataFrame.
    
    Args:
        file_path (str): Path to the WhatsApp chat export file
        
    Returns:
        pd.DataFrame: DataFrame with columns [datetime, sender, message, date, time, hour]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Try with a different encoding if utf-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    # WhatsApp chat format regex pattern
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?\s?[APMapm]{2}?)\s-\s([^:]+):\s(.*)'
    
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    # Create DataFrame
    df = pd.DataFrame(matches, columns=['datetime', 'sender', 'message'])
    
    # Clean sender names
    df['sender'] = df['sender'].str.strip()
    
    # Try multiple datetime formats
    datetime_formats = [
        '%m/%d/%y, %I:%M %p',  # US format
        '%d/%m/%Y, %H:%M:%S',  # International format
        '%d/%m/%y, %I:%M %p',  # UK format
        '%m/%d/%Y, %I:%M:%S %p'  # US format with seconds
    ]
    
    for dt_format in datetime_formats:
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], format=dt_format)
            if not df['datetime'].isna().any():
                break
        except:
            continue
    
    # Extract components
    df['date'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.time
    df['hour'] = df['datetime'].dt.hour
    
    # Remove system messages
    df = df.dropna(subset=['datetime'])
    
    return df