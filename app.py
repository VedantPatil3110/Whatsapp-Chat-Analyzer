from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.chat_parser import parse_whatsapp_chat
from utils.analyzers import get_top_words, get_top_emojis, get_hourly_activity

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/analyze', methods=['POST'])
def analyze_chat():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        try:
            # Parse the chat file
            df = parse_whatsapp_chat(file_path)
            
            # Perform analysis
            analysis_result = {
                'topWords': get_top_words(df),
                'topEmojis': get_top_emojis(df),
                'hourlyActivity': get_hourly_activity(df),
                'totalMessages': len(df),
                'totalWords': sum(len(msg.split()) for msg in df['message']),
                'totalEmojis': sum(len([c for c in msg if c in emoji.EMOJI_DATA]) for msg in df['message']),
                'startDate': df['date'].min().strftime('%Y-%m-%d'),
                'endDate': df['date'].max().strftime('%Y-%m-%d'),
                'participants': df['sender'].unique().tolist()
            }
            
            # Clean up
            os.remove(file_path)
            
            return jsonify(analysis_result)
        
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)