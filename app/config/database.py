from mysql.connector import pooling

class DatabaseConfig:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "gamification_testing",
            "port": 3306
        }
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **self.config
        )

    def get_connection(self):
        return self.pool.get_connection()