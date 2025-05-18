from mysql.connector import pooling
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "gamification_testing"),
            "port": int(os.getenv("DB_PORT", "3306"))
        }
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **self.config
        )

    def get_connection(self):
        return self.pool.get_connection()