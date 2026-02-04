import sqlite3
from typing import Optional
from datetime import datetime
from ..models.user import User
from ..database.connection import DatabaseConnection


class UserRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def create(self, username: str, password: str, role: str = "staff") -> Optional[User]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.conn.commit()
            
            user_id = cursor.lastrowid
            cursor.close()
            
            return User(
                username=username,
                password=password,
                role=role,
                user_id=user_id,
                created_at=datetime.now()
            )
        except sqlite3.IntegrityError:
            return None
    
    def find_by_credentials(self, username: str, password: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return User(
                username=row['username'],
                password=row['password'],
                role=row['role'],
                user_id=row['id'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
