# dao/user_dao.py
from config.database  import get_connection
from models.user import User

class UserDAO:
    @staticmethod
    def login(username, password):
        conn = get_connection()
        cur = conn.cursor()
        # NOTE: In real projects hash the password! For assignment plain text is accepted.
        cur.execute("""
            SELECT u.user_id, u.username, u.role, m.member_id
            FROM users u
            LEFT JOIN members m ON LOWER(u.username) = LOWER(m.email)
            WHERE LOWER(u.username) = LOWER(%s) AND u.password = %s
        """, (username, password))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return User(row['user_id'], row['username'], row['role'], row['member_id'])
        return None