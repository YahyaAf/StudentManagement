from typing import Optional, List
from datetime import date
from ..models.student import Student
from ..repositories.student_repository import StudentRepository


class StudentService:
    
    def __init__(self):
        self.repository = StudentRepository()
    
    def create(self, first_name: str, last_name: str, email: str, 
               phone: str, date_of_birth: date, class_id: int) -> Optional[Student]:
        return self.repository.create(first_name, last_name, email, phone, date_of_birth, class_id)
    
    def get_by_id(self, student_id: int) -> Optional[Student]:
        return self.repository.get_by_id(student_id)
    
    def get_all(self) -> List[Student]:
        return self.repository.get_all()
    
    def get_all_with_class(self) -> List[dict]:
        return self.repository.get_all_with_class()
    
    def update(self, student_id: int, first_name: Optional[str] = None, 
               last_name: Optional[str] = None, email: Optional[str] = None,
               phone: Optional[str] = None, date_of_birth: Optional[date] = None,
               class_id: Optional[int] = None) -> bool:
        return self.repository.update(student_id, first_name, last_name, email, phone, date_of_birth, class_id)
    
    def delete(self, student_id: int) -> bool:
        return self.repository.delete(student_id)
