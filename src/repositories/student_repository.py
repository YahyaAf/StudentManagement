import sqlite3
from typing import Optional, List
from datetime import datetime, date
from ..models.student import Student
from ..database.connection import DatabaseConnection


class StudentRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def create(self, first_name: str, last_name: str, email: str, 
               phone: str, date_of_birth: date, class_id: int) -> Optional[Student]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO students (first_name, last_name, email, phone, date_of_birth, class_id) VALUES (?, ?, ?, ?, ?, ?)",
                (first_name, last_name, email, phone, date_of_birth.isoformat(), class_id)
            )
            self.conn.commit()
            
            student_id = cursor.lastrowid
            cursor.close()
            
            return Student(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                date_of_birth=date_of_birth,
                class_id=class_id,
                student_id=student_id,
                created_at=datetime.now()
            )
        except sqlite3.IntegrityError:
            return None
    
    def get_by_id(self, student_id: int) -> Optional[Student]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return Student(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone=row['phone'],
                date_of_birth=date.fromisoformat(row['date_of_birth']),
                class_id=row['class_id'],
                student_id=row['id'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
    
    def get_all(self) -> List[Student]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()
        
        students = []
        for row in rows:
            student = Student(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone=row['phone'],
                date_of_birth=date.fromisoformat(row['date_of_birth']),
                class_id=row['class_id'],
                student_id=row['id'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
            students.append(student)
        return students
    
    def get_all_with_class(self) -> List[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                s.id, s.first_name, s.last_name, s.email, s.phone, 
                s.date_of_birth, s.class_id, s.created_at,
                c.name as class_name, c.level as class_level, c.year as class_year
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
        """)
        rows = cursor.fetchall()
        cursor.close()
        
        results = []
        for row in rows:
            result = {
                'student': Student(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    phone=row['phone'],
                    date_of_birth=date.fromisoformat(row['date_of_birth']),
                    class_id=row['class_id'],
                    student_id=row['id'],
                    created_at=datetime.fromisoformat(row['created_at'])
                ),
                'class_name': row['class_name'],
                'class_level': row['class_level'],
                'class_year': row['class_year']
            }
            results.append(result)
        return results
    
    def update(self, student_id: int, first_name: Optional[str] = None, 
               last_name: Optional[str] = None, email: Optional[str] = None,
               phone: Optional[str] = None, date_of_birth: Optional[date] = None,
               class_id: Optional[int] = None) -> bool:
        cursor = self.conn.cursor()
        
        if first_name:
            cursor.execute("UPDATE students SET first_name = ? WHERE id = ?", (first_name, student_id))
        if last_name:
            cursor.execute("UPDATE students SET last_name = ? WHERE id = ?", (last_name, student_id))
        if email:
            cursor.execute("UPDATE students SET email = ? WHERE id = ?", (email, student_id))
        if phone:
            cursor.execute("UPDATE students SET phone = ? WHERE id = ?", (phone, student_id))
        if date_of_birth:
            cursor.execute("UPDATE students SET date_of_birth = ? WHERE id = ?", (date_of_birth.isoformat(), student_id))
        if class_id:
            cursor.execute("UPDATE students SET class_id = ? WHERE id = ?", (class_id, student_id))
        
        self.conn.commit()
        cursor.close()
        return True
    
    def delete(self, student_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        return deleted
