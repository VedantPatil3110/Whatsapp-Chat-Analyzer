# Whatsapp-Chat-Analyzer
WhatsApp Chat Analyzer is a full-stack web app that provides deep insights into your WhatsApp conversations.
Upload your exported .txt chat file, and get visual analytics on message frequency, word usage, emoji trends, and activity patterns — all in a clean, interactive dashboard.

🚀 Features

📄 Chat Parsing: Automatically parses exported WhatsApp .txt files

🧠 Data Insights:

Total messages, words, emojis, and participants

Top used words and emojis

Hourly activity distribution

📊 Interactive Charts: Built with Chart.js for smooth, responsive visualization

⚡ Full-Stack Setup:

Backend: Flask (Python) for file upload, parsing, and data analysis

Frontend: HTML, CSS, and JavaScript for UI and visualization

🔍 Real-Time Analysis: No database needed — everything runs locally

🧩 Emoji & Word Frequency Detection: Intelligent text cleaning and filtering

🛠️ Tech Stack
Layer	Technologies
Frontend	HTML5, CSS3, JavaScript, Chart.js
Backend	Flask, pandas, emoji, regex
Data Handling	pandas DataFrame, Counter, regex parsing
Styling	Custom CSS (responsive, minimal UI)
📂 Project Structure
📁 whatsapp-chat-analyzer/
│
├── app.py                # Flask backend API
├── utils/
│   ├── chat_parser.py    # Parses WhatsApp chat files into structured data
│   └── analyzers.py      # Performs word, emoji, and time-based analysis
│
├── static/
│   ├── css/style.css     # UI styling
│   ├── js/app.js         # Frontend logic and chart rendering
│   └── images/upload.svg # Upload icon
│
├── templates/
│   └── index.html        # Main web interface
│
└── README.md             # (You are here)

⚙️ How It Works

Export your WhatsApp chat as a .txt file (without media).

Upload it through the web interface.

The Flask backend parses and analyzes the data.

View interactive charts showing your top words, emojis, and chat activity timeline.

📸 Example Insights

Top Words: “okay”, “yes”, “thanks”

Top Emojis: 😂 ❤️ 👍

Active Hours: Most messages sent at 9 PM

🧑‍💻 Local Setup
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py


Then open http://localhost:5000
 in your browser.

💡 Future Enhancements

Conversation sentiment analysis

Per-user message breakdown

Word cloud visualization

Export results as CSV or image

🏷️ License

This project is licensed under the MIT License — free to use and modify.
