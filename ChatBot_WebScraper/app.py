from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from scraper import get_latest_news

nltk.download('punkt')

app = Flask(__name__)

def process_user_input(user_input):
    tokens = word_tokenize(user_input.lower())
    # Simple intent recognition
    if 'news' in tokens:
        # Extract topic
        topics = [word for word in tokens if word not in ['get', 'latest', 'news', 'tell', 'me', 'about']]
        topic = ' '.join(topics) if topics else 'world'
        return {'intent': 'get_news', 'topic': topic}
    else:
        return {'intent': 'unknown', 'message': "I'm sorry, I can help you fetch the latest news. Try asking something like 'Get me the latest news on technology'."}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=['POST'])
def chat():
    user_message = request.form['message']
    response = process_user_input(user_message)

    if response['intent'] == 'get_news':
        news = get_latest_news(response['topic'])
        if isinstance(news, str):
            bot_response = news
        else:
            bot_response = "Here are the latest news articles:\n"
            for item in news:
                bot_response += f"- {item['title']} ({item['link']})\n"
    else:
        bot_response = response['message']

    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
