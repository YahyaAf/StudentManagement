import sqlite3
from typing import Optional, List
from datetime import datetime
from ..models.subject import Subject
from ..database.connection import DatabaseConnection


class SubjectRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def create(self, name: str, coefficient: float) -> Optional[Subject]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO subjects (name, coefficient) VALUES (?, ?)",
                (name, coefficient)
            )
            self.conn.commit()
            
            subject_id = cursor.lastrowid
            cursor.close()
            
            return Subject(
                name=name,
                coefficient=coefficient,
                subject_id=subject_id,
                created_at=datetime.now()
            )
        except sqlite3.IntegrityError:
            return None
    
    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,))
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return Subject(
                name=row['name'],
                coefficient=row['coefficient'],
                subject_id=row['id'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
    
    def get_all(self) -> List[Subject]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM subjects")
        rows = cursor.fetchall()
        cursor.close()
        
        subjects = []
        for row in rows:
            subject = Subject(
                name=row['name'],
                coefficient=row['coefficient'],
                subject_id=row['id'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
            subjects.append(subject)
        return subjects
    
    def update(self, subject_id: int, name: Optional[str] = None, 
               coefficient: Optional[float] = None) -> bool:
        cursor = self.conn.cursor()
        
        if name:
            cursor.execute("UPDATE subjects SET name = ? WHERE id = ?", (name, subject_id))
        if coefficient:
            cursor.execute("UPDATE subjects SET coefficient = ? WHERE id = ?", (coefficient, subject_id))
        
        self.conn.commit()
        cursor.close()
        return True
    
    def delete(self, subject_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        self.conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        return deleted
