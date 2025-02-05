import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from config import Config

class DatabaseManager:
    def __init__(self):
        self.init_db()

    @contextmanager
    def get_cursor(self):
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            cursor_factory=DictCursor
        )
        try:
            yield conn.cursor()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_db(self):
        """Initialize database tables if they don't exist"""
        with self.get_cursor() as cur:
            # Create users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create sticker_usage table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sticker_usage (
                    usage_id SERIAL PRIMARY KEY,
                    user_id BIGINT REFERENCES users(user_id),
                    sticker_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Database tables initialized successfully")

    def log_sticker_usage(self, user_data, sticker_id):
        with self.get_cursor() as cur:
            # Insert or update user
            cur.execute("""
                INSERT INTO users (user_id, username, first_name, last_name)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE 
                SET username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name
            """, (user_data['id'], user_data.get('username'), 
                  user_data.get('first_name'), user_data.get('last_name')))

            # Log sticker usage
            cur.execute("""
                INSERT INTO sticker_usage (user_id, sticker_id)
                VALUES (%s, %s)
            """, (user_data['id'], sticker_id))

    def get_stats(self):
        with self.get_cursor() as cur:
            # Get sticker stats with user details
            cur.execute("""
                SELECT 
                    su.sticker_id,
                    COUNT(*) as total_sends,
                    array_agg(DISTINCT u.username) as top_users
                FROM sticker_usage su
                JOIN users u ON su.user_id = u.user_id
                GROUP BY su.sticker_id
                ORDER BY total_sends DESC
                LIMIT 10
            """)
            sticker_stats = cur.fetchall()

            # Get user stats with usernames
            cur.execute("""
                SELECT 
                    u.username,
                    u.first_name,
                    COUNT(*) as sends,
                    array_agg(DISTINCT su.sticker_id) as favorite_stickers
                FROM sticker_usage su
                JOIN users u ON su.user_id = u.user_id
                GROUP BY u.user_id, u.username, u.first_name
                ORDER BY sends DESC
                LIMIT 10
            """)
            user_stats = cur.fetchall()

            return {
                'sticker_stats': [dict(row) for row in sticker_stats],
                'user_stats': [dict(row) for row in user_stats]
            } 