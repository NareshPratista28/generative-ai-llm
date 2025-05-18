from app.config.database import DatabaseConfig

class LessonModel:
    def __init__(self):
        self.db = DatabaseConfig()

    def get_prompt_and_description(self, content_id: int):
        """
        Mengambil prompt_llm dan materi pembelajaran dari tabel content berdasarkan content_id
        
        Args:
            content_id: ID konten pembelajaran
            
        Returns:
            Dictionary berisi prompt_llm, content_text, dan title atau None jika tidak ditemukan
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT prompt_llm, description, title FROM contents WHERE id = %s", (content_id,))
            result = cursor.fetchone()
            return result if result else None
        finally:
            cursor.close()
            conn.close()