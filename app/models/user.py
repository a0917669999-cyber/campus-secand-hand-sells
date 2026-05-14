import sqlite3
from flask import current_app
from werkzeug.security import generate_password_hash

def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

class User:
    @staticmethod
    def create(email, password):
        """新增一筆使用者記錄"""
        conn = get_db_connection()
        try:
            password_hash = generate_password_hash(password)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (email, password_hash) VALUES (?, ?)',
                (email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Email already exists
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        """根據信箱取得使用者"""
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            return user
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """取得單筆使用者記錄"""
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return user
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(user_id, email=None, password=None):
        """更新使用者記錄"""
        conn = get_db_connection()
        try:
            updates = []
            params = []
            if email:
                updates.append('email = ?')
                params.append(email)
            if password:
                updates.append('password_hash = ?')
                params.append(generate_password_hash(password))
            
            if not updates:
                return False

            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            conn.execute(query, tuple(params))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        """刪除使用者記錄"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            conn.close()
