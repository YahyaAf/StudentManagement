from typing import Optional, List
from ..models.grade import Grade
from ..repositories.grade_repository import GradeRepository


class GradeService:
    
    def __init__(self, repository: GradeRepository):
        self.repository = repository
    
    def create(self, student_id: int, subject_id: int, grade: float) -> Optional[Grade]:
        return self.repository.create(student_id, subject_id, grade)
    
    def get_grades_by_student(self, student_id: int) -> List[dict]:
        return self.repository.get_grades_by_student(student_id)
    
    def get_all_students_with_grades(self) -> List[dict]:
        return self.repository.get_all_students_with_grades()
    
    def get_students_by_subject(self, subject_id: int) -> List[dict]:
        return self.repository.get_students_by_subject(subject_id)
