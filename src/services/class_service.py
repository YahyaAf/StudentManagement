from typing import Optional, List
from ..models.class_model import Class
from ..repositories.class_repository import ClassRepository


class ClassService:
    
    def __init__(self, repository: ClassRepository):
        self.repository = repository
    
    def create(self, name: str, level: str, year: str) -> Optional[Class]:
        return self.repository.create(name, level, year)
    
    def get_by_id(self, class_id: int) -> Optional[Class]:
        return self.repository.get_by_id(class_id)
    
    def get_all(self) -> List[Class]:
        return self.repository.get_all()
    
    def update(self, class_id: int, name: Optional[str] = None, 
               level: Optional[str] = None, year: Optional[str] = None) -> bool:
        return self.repository.update(class_id, name, level, year)
    
    def delete(self, class_id: int) -> bool:
        return self.repository.delete(class_id)
