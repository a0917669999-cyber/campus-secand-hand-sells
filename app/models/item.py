import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Item:
    @staticmethod
    def create(data):
        """新增一筆商品記錄"""
        pass

    @staticmethod
    def get_all():
        """取得所有商品記錄"""
        pass

    @staticmethod
    def search_and_filter(query=None, category=None, min_price=None, max_price=None):
        """根據關鍵字、分類、價格區間進行搜尋與過濾 (F-04)"""
        pass

    @staticmethod
    def get_by_id(item_id):
        """取得單筆商品記錄"""
        pass

    @staticmethod
    def update(item_id, data):
        """更新商品記錄"""
        pass

    @staticmethod
    def update_status(item_id, status):
        """更新商品狀態 (available/sold)"""
        pass

    @staticmethod
    def delete(item_id):
        """刪除商品記錄"""
        pass
