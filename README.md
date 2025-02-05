# Telegram Sticker Analytics Bot

A Flask-based web application that tracks and analyzes sticker usage in Telegram chats. The bot monitors sticker sends and provides statistics about most used stickers and top sticker users.

## Features

- Track sticker usage in Telegram chats
- Record user information and sticker sends
- Display statistics about most used stickers
- Show top users and their favorite stickers
- Real-time updates through webhook integration

## Prerequisites

- Python 3.7+
- PostgreSQL database
- ngrok (for local development)
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

## Installation

1. Clone the repository:
bash
git clone https://github.com/zhans1/tg_stiker_analyze.git
cd telegram-sticker-analytics

2. Install required packages:
bash
pip install flask psycopg2-binary requests python-dotenv

3. Create PostgreSQL database:
sql
CREATE DATABASE telegram_stickers;

## Configuration

1. Update `config.py` with your settings:
python
TELEGRAM_BOT_TOKEN = 'your-bot-token'
DB_HOST = 'localhost'
DB_NAME = 'telegram_stickers'
DB_USER = 'your-db-user'
DB_PASSWORD = 'your-db-password'

## Running the Application

1. Start ngrok (in a separate terminal):
bash
ngrok http 5000

2. Copy the HTTPS URL provided by ngrok (e.g., https://xxxx-xx-xx-xxx-xx.ngrok-free.app)

3. Run the Flask application:
bash
python app.py

4. When prompted, paste the ngrok HTTPS URL

5. Add your bot to a Telegram group and start sending stickers!

## API Endpoints

- `/` - Web interface showing sticker statistics
- `/webhook` - Telegram webhook endpoint
- `/stats` - JSON API for sticker usage statistics

## Database Schema

### Users Table
sql
CREATE TABLE users (
user_id BIGINT PRIMARY KEY,
username TEXT,
first_name TEXT,
last_name TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

### Sticker Usage Table
sql
CREATE TABLE sticker_usage (
usage_id SERIAL PRIMARY KEY,
user_id BIGINT REFERENCES users(user_id),
sticker_id TEXT,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## Development Notes

- The application uses ngrok for local development to provide a public HTTPS URL
- Database tables are automatically created on first run
- The web interface refreshes statistics every minute
- Webhook updates are processed in real-time

## Troubleshooting

1. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Verify database credentials in config.py
   - Check if database exists

2. **Webhook Errors**
   - Make sure ngrok is running
   - Verify HTTPS URL is correctly set
   - Check Telegram bot token

3. **Missing Statistics**
   - Confirm bot has necessary permissions in group
   - Verify webhook is receiving updates
   - Check database for stored data

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request