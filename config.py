import os

class Config:
    TELEGRAM_BOT_TOKEN = '6931484907:AAHkSpe01TCywyqDT7ehej2HUMmVk0l-N2I'
    DB_HOST = 'localhost'
    DB_NAME = 'telegram_stickers'
    DB_USER = 'postgres'
    DB_PASSWORD = '123123'
    
    # Local development settings
    WEBHOOK_HOST = 'http://localhost:5000'  # Changed to localhost
    WEBHOOK_PATH = '/webhook'
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" 