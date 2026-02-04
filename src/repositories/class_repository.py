import sqlite3
from typing import Optional, List
from datetime import datetime
from ..models.class_model import Class
from ..database.connection import DatabaseConnection


class ClassRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def create(self, name: str, level: str, year: str) -> Optional[Class]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO classes (name, level, year) VALUES (?, ?, ?)",
                (name, level, year)
            )
            self.conn.commit()
            
            class_id = cursor.lastrowid
            cursor.close()
            
            return Class(
                name=name,
                level=level,
                year=year,
                class_id=class_id,
                created_at=datetime.now()
            )
        except sqlite3.IntegrityError:
            return None
    
    def get_by_id(self, class_id: int) -> Optional[Class]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM classes WHERE id = ?", (class_id,))
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return Class(
                name=row['name'],
                level=row['level'],
                year=row['year'],
                class_id=row['id'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
    
    def get_all(self) -> List[Class]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM classes")
        rows = cursor.fetchall()
        cursor.close()
        
        classes = []
        for row in rows:
            class_obj = Class(
                name=row['name'],
                level=row['level'],
                year=row['year'],
                class_id=row['id'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
            classes.append(class_obj)
        return classes
    
    def update(self, class_id: int, name: Optional[str] = None, 
               level: Optional[str] = None, year: Optional[str] = None) -> bool:
        cursor = self.conn.cursor()
        
        if name:
            cursor.execute("UPDATE classes SET name = ? WHERE id = ?", (name, class_id))
        if level:
            cursor.execute("UPDATE classes SET level = ? WHERE id = ?", (level, class_id))
        if year:
            cursor.execute("UPDATE classes SET year = ? WHERE id = ?", (year, class_id))
        
        self.conn.commit()
        cursor.close()
        return True
    
    def delete(self, class_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        self.conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        return deleted
