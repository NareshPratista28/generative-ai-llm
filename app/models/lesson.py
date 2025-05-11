from app.config.database import DatabaseConfig

class LessonModel:
    def __init__(self):
        self.db = DatabaseConfig()

    def get_prompt(self, content_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT prompt_llm FROM lessons WHERE id = %s", (content_id,))
            result = cursor.fetchone()
            return result['prompt_llm'] if result else None
        finally:
            cursor.close()
            conn.close()