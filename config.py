import os

class Config:
    TELEGRAM_BOT_TOKEN = 'TOKEN'
    DB_HOST = 'localhost'
    DB_NAME = 'telegram_stickers'
    DB_USER = 'postgres'
    DB_PASSWORD = 'PASS'
    
    # Local development settings
    WEBHOOK_HOST = 'http://localhost:5000'  # Changed to localhost
    WEBHOOK_PATH = '/webhook'
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" 
