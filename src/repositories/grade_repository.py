import sqlite3
from typing import Optional, List
from datetime import datetime, date
from ..models.grade import Grade
from ..database.connection import DatabaseConnection


class GradeRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def create(self, student_id: int, subject_id: int, grade: float) -> Optional[Grade]:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO grades (student_id, subject_id, grade) VALUES (?, ?, ?)",
                (student_id, subject_id, grade)
            )
            self.conn.commit()
            
            grade_id = cursor.lastrowid
            cursor.close()
            
            return Grade(
                student_id=student_id,
                subject_id=subject_id,
                grade=grade,
                grade_id=grade_id,
                created_at=datetime.now()
            )
        except sqlite3.IntegrityError:
            return None
    
    def get_grades_by_student(self, student_id: int) -> List[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                g.id, g.grade, g.created_at,
                s.id as student_id, s.first_name, s.last_name, s.email,
                sub.id as subject_id, sub.name as subject_name, sub.coefficient
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            WHERE g.student_id = ?
        """, (student_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        results = []
        for row in rows:
            result = {
                'grade_id': row['id'],
                'grade': row['grade'],
                'created_at': row['created_at'],
                'student_id': row['student_id'],
                'student_name': f"{row['first_name']} {row['last_name']}",
                'student_email': row['email'],
                'subject_id': row['subject_id'],
                'subject_name': row['subject_name'],
                'coefficient': row['coefficient']
            }
            results.append(result)
        return results
    
    def get_all_students_with_grades(self) -> List[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                s.id as student_id, s.first_name, s.last_name, s.email,
                c.name as class_name, c.level as class_level,
                g.id as grade_id, g.grade,
                sub.name as subject_name, sub.coefficient
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN grades g ON s.id = g.student_id
            LEFT JOIN subjects sub ON g.subject_id = sub.id
            ORDER BY s.id, sub.name
        """)
        rows = cursor.fetchall()
        cursor.close()
        
        students_dict = {}
        for row in rows:
            student_id = row['student_id']
            if student_id not in students_dict:
                students_dict[student_id] = {
                    'student_id': student_id,
                    'student_name': f"{row['first_name']} {row['last_name']}",
                    'email': row['email'],
                    'class_name': row['class_name'],
                    'class_level': row['class_level'],
                    'grades': []
                }
            
            if row['grade_id']:
                students_dict[student_id]['grades'].append({
                    'grade_id': row['grade_id'],
                    'subject_name': row['subject_name'],
                    'coefficient': row['coefficient'],
                    'grade': row['grade']
                })
        
        return list(students_dict.values())
    
    def get_students_by_subject(self, subject_id: int) -> List[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                g.id as grade_id, g.grade, g.created_at,
                s.id as student_id, s.first_name, s.last_name, s.email,
                c.name as class_name,
                sub.id as subject_id, sub.name as subject_name, sub.coefficient
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            LEFT JOIN classes c ON s.class_id = c.id
            WHERE g.subject_id = ?
            ORDER BY s.last_name, s.first_name
        """, (subject_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        results = []
        for row in rows:
            result = {
                'grade_id': row['grade_id'],
                'grade': row['grade'],
                'created_at': row['created_at'],
                'student_id': row['student_id'],
                'student_name': f"{row['first_name']} {row['last_name']}",
                'student_email': row['email'],
                'class_name': row['class_name'],
                'subject_id': row['subject_id'],
                'subject_name': row['subject_name'],
                'coefficient': row['coefficient']
            }
            results.append(result)
        return results
