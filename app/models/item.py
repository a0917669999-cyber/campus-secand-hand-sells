import sqlite3
from flask import current_app

def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

class Item:
    @staticmethod
    def create(seller_id, title, description, category, brand, condition, price, ai_price_min=None, ai_price_max=None):
        """新增一筆商品記錄"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO items 
                   (seller_id, title, description, category, brand, condition, price, ai_price_min, ai_price_max) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (seller_id, title, description, category, brand, condition, price, ai_price_min, ai_price_max)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating item: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有商品記錄 (預設只顯示 available)"""
        conn = get_db_connection()
        try:
            items = conn.execute(
                'SELECT items.*, users.email as seller_email FROM items JOIN users ON items.seller_id = users.id WHERE status = "available" ORDER BY items.created_at DESC'
            ).fetchall()
            return items
        except Exception as e:
            print(f"Error getting all items: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def search_and_filter(query=None, category=None, min_price=None, max_price=None):
        """根據關鍵字、分類、價格區間進行搜尋與過濾 (F-04)"""
        conn = get_db_connection()
        try:
            sql = 'SELECT items.*, users.email as seller_email FROM items JOIN users ON items.seller_id = users.id WHERE status = "available"'
            params = []

            if query:
                sql += ' AND (title LIKE ? OR description LIKE ?)'
                params.extend([f'%{query}%', f'%{query}%'])
            
            if category:
                sql += ' AND category = ?'
                params.append(category)

            if min_price is not None and str(min_price).strip() != '':
                sql += ' AND price >= ?'
                params.append(int(min_price))

            if max_price is not None and str(max_price).strip() != '':
                sql += ' AND price <= ?'
                params.append(int(max_price))

            sql += ' ORDER BY items.created_at DESC'

            items = conn.execute(sql, tuple(params)).fetchall()
            return items
        except Exception as e:
            print(f"Error searching items: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(item_id):
        """取得單筆商品記錄"""
        conn = get_db_connection()
        try:
            item = conn.execute(
                'SELECT items.*, users.email as seller_email FROM items JOIN users ON items.seller_id = users.id WHERE items.id = ?', 
                (item_id,)
            ).fetchone()
            return item
        except Exception as e:
            print(f"Error getting item by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(item_id, seller_id, title, description, category, brand, condition, price):
        """更新商品記錄 (限制只有發布者可以更新)"""
        conn = get_db_connection()
        try:
            conn.execute(
                '''UPDATE items SET title=?, description=?, category=?, brand=?, condition=?, price=?
                   WHERE id=? AND seller_id=?''',
                (title, description, category, brand, condition, price, item_id, seller_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating item: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_status(item_id, seller_id, status):
        """更新商品狀態 (available/sold)"""
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE items SET status=? WHERE id=? AND seller_id=?',
                (status, item_id, seller_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating item status: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(item_id, seller_id):
        """刪除商品記錄"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM items WHERE id=? AND seller_id=?', (item_id, seller_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False
        finally:
            conn.close()
