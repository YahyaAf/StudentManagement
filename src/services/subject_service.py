from typing import Optional, List
from ..models.subject import Subject
from ..repositories.subject_repository import SubjectRepository


class SubjectService:
    
    def __init__(self):
        self.repository = SubjectRepository()
    
    def create(self, name: str, coefficient: float) -> Optional[Subject]:
        return self.repository.create(name, coefficient)
    
    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        return self.repository.get_by_id(subject_id)
    
    def get_all(self) -> List[Subject]:
        return self.repository.get_all()
    
    def update(self, subject_id: int, name: Optional[str] = None, 
               coefficient: Optional[float] = None) -> bool:
        return self.repository.update(subject_id, name, coefficient)
    
    def delete(self, subject_id: int) -> bool:
        return self.repository.delete(subject_id)
