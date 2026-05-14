import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class User:
    @staticmethod
    def create(email, password_hash):
        """新增一筆使用者記錄"""
        pass

    @staticmethod
    def get_by_email(email):
        """根據信箱取得使用者"""
        pass

    @staticmethod
    def get_by_id(user_id):
        """取得單筆使用者記錄"""
        pass

    @staticmethod
    def update(user_id, data):
        """更新使用者記錄"""
        pass

    @staticmethod
    def delete(user_id):
        """刪除使用者記錄"""
        pass
