from app.config.database import DatabaseConfig
import json
import time

class GenerationHistory:
    def __init__(self):
        self.db = DatabaseConfig()
    
    def save_generation(self, content_id: int, topic_title: str, result: dict, generation_time: float) -> int:
        """
        Menyimpan hasil generasi soal ke dalam database.
        
        Args:
            content_id: ID konten pembelajaran
            topic_title: Judul/topik materi
            result: Dictionary hasil generasi (raw_response, code, studi_kasus, tugas)
            generation_time: Waktu pemrosesan dalam detik
            
        Returns:
            ID history yang tersimpan atau 0 jika gagal
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Konversi hasil ke JSON untuk penyimpanan
            result_json = json.dumps(result, ensure_ascii=False)
            
            # Ambil timestamp sekarang
            created_at = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Simpan ke database
            query = """
                INSERT INTO generation_history 
                (content_id, topic_title, result, generation_time, created_at) 
                VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (content_id, topic_title, result_json, generation_time, created_at))
            conn.commit()
            
            # Ambil ID yang baru saja dimasukkan
            history_id = cursor.lastrowid
            return history_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def get_history_by_id(self, history_id: int) -> dict:
        """
        Mengambil detail history berdasarkan ID.
        
        Args:
            history_id: ID history
            
        Returns:
            Dictionary berisi detail history atau None jika tidak ditemukan
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT h.id, h.content_id, c.title as content_title, 
                       h.topic_title, h.result, h.generation_time, h.created_at
                FROM generation_history h
                JOIN contents c ON h.content_id = c.id
                WHERE h.id = %s
            """
            
            cursor.execute(query, (history_id,))
            result = cursor.fetchone()
            
            if result and 'result' in result:
                # Parse JSON result
                result['result'] = json.loads(result['result'])
            
            return result
            
        finally:
            cursor.close()
            conn.close()
    
    def get_history_list(self, limit: int = 20, offset: int = 0) -> list:
        """
        Mengambil daftar history generasi.
        
        Args:
            limit: Jumlah maksimum record yang diambil
            offset: Offset untuk pagination
            
        Returns:
            List dictionary berisi history
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT h.id, h.content_id, c.title as content_title, 
                       h.topic_title, h.generation_time, h.created_at
                FROM generation_history h
                JOIN contents c ON h.content_id = c.id
                ORDER BY h.created_at DESC
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, (limit, offset))
            results = cursor.fetchall()
            
            return results
            
        finally:
            cursor.close()
            conn.close()
    
    def get_history_by_content_id(self, content_id: int, limit: int = 10) -> list:
        """
        Mengambil daftar history generasi untuk konten tertentu.
        
        Args:
            content_id: ID konten pembelajaran
            limit: Jumlah maksimum record yang diambil
            
        Returns:
            List dictionary berisi history
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT h.id, h.content_id, c.title as content_title,
                       h.topic_title, h.generation_time, h.created_at
                FROM generation_history h
                JOIN contents c ON h.content_id = c.id
                WHERE h.content_id = %s
                ORDER BY h.created_at DESC
                LIMIT %s
            """
            
            cursor.execute(query, (content_id, limit))
            results = cursor.fetchall()
            
            return results
            
        finally:
            cursor.close()
            conn.close()
            
    def search_history(self, search_term: str, limit: int = 20, offset: int = 0) -> list:
        """
        Mencari history generasi berdasarkan judul topik.
        
        Args:
            search_term: Kata kunci pencarian untuk judul topik
            limit: Jumlah maksimum record yang diambil
            offset: Offset untuk pagination
            
        Returns:
            List dictionary berisi history yang sesuai
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
                SELECT h.id, h.content_id, c.title as content_title, 
                       h.topic_title, h.generation_time, h.created_at
                FROM generation_history h
                JOIN contents c ON h.content_id = c.id
                WHERE h.topic_title LIKE %s
                ORDER BY h.created_at DESC
                LIMIT %s OFFSET %s
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, limit, offset))
            results = cursor.fetchall()
            
            return results
            
        finally:
            cursor.close()
            conn.close()