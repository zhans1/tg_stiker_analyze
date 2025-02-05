from flask import Flask, request, jsonify, render_template
from database import DatabaseManager
from config import Config
import requests
import os

app = Flask(__name__)
db = DatabaseManager()

def setup_webhook():
    """Set up the Telegram webhook using ngrok URL"""
    try:
        # Get the public HTTPS URL from ngrok
        ngrok_url = input("Please enter your ngrok HTTPS URL: ")
        webhook_url = f"{ngrok_url}/webhook"
        
        url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/setWebhook"
        response = requests.post(url, json={'url': webhook_url})
        print(f"Webhook set to: {webhook_url}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error setting up webhook: {str(e)}")
        return None

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        message = data.get('message')

        if message and message.get('sticker'):
            user = message['from']
            sticker = message['sticker']
            db.log_sticker_usage(user, sticker['file_id'])

        return jsonify({'status': 'ok'})
    except Exception as e:
        app.logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stats')
def stats():
    try:
        return jsonify(db.get_stats())
    except Exception as e:
        app.logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    setup_webhook()
    app.run(debug=True, port=5000) 