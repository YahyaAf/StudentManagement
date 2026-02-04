from typing import Optional
from datetime import datetime


class Grade:
    
    def __init__(
        self,
        student_id: int,
        subject_id: int,
        grade: float,
        grade_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self._id = grade_id
        self._student_id = student_id
        self._subject_id = subject_id
        self._grade = grade
        self._created_at = created_at or datetime.now()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @property
    def student_id(self) -> int:
        return self._student_id
    
    @student_id.setter
    def student_id(self, value: int):
        if not value:
            raise ValueError("Le student_id ne peut pas etre vide")
        self._student_id = value
    
    @property
    def subject_id(self) -> int:
        return self._subject_id
    
    @subject_id.setter
    def subject_id(self, value: int):
        if not value:
            raise ValueError("Le subject_id ne peut pas etre vide")
        self._subject_id = value
    
    @property
    def grade(self) -> float:
        return self._grade
    
    @grade.setter
    def grade(self, value: float):
        if value < 0 or value > 20:
            raise ValueError("La note doit etre entre 0 et 20")
        self._grade = value
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def __str__(self) -> str:
        return f"Grade(id={self._id}, student_id={self._student_id}, subject_id={self._subject_id}, grade={self._grade})"
    
    def __repr__(self) -> str:
        return (f"Grade(grade_id={self._id}, student_id={self._student_id}, "
                f"subject_id={self._subject_id}, grade={self._grade}, created_at='{self._created_at}')")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Grade):
            return False
        return self._id == other._id
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "student_id": self._student_id,
            "subject_id": self._subject_id,
            "grade": self._grade,
            "created_at": self._created_at.isoformat() if self._created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Grade':
        created_at = None
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'])
            else:
                created_at = data['created_at']
        
        return cls(
            student_id=data['student_id'],
            subject_id=data['subject_id'],
            grade=data['grade'],
            grade_id=data.get('id'),
            created_at=created_at
        )
