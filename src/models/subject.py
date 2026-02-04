from typing import Optional
from datetime import datetime


class Subject:
    
    def __init__(
        self,
        name: str,
        coefficient: float,
        subject_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self._id = subject_id
        self._name = name
        self._coefficient = coefficient
        self._created_at = created_at or datetime.now()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value or len(value) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caracteres")
        self._name = value
    
    @property
    def coefficient(self) -> float:
        return self._coefficient
    
    @coefficient.setter
    def coefficient(self, value: float):
        if value <= 0:
            raise ValueError("Le coefficient doit etre superieur a 0")
        self._coefficient = value
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def __str__(self) -> str:
        return f"Subject(id={self._id}, name='{self._name}', coefficient={self._coefficient})"
    
    def __repr__(self) -> str:
        return (f"Subject(subject_id={self._id}, name='{self._name}', "
                f"coefficient={self._coefficient}, created_at='{self._created_at}')")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Subject):
            return False
        return self._id == other._id
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "coefficient": self._coefficient,
            "created_at": self._created_at.isoformat() if self._created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Subject':
        created_at = None
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'])
            else:
                created_at = data['created_at']
        
        return cls(
            name=data['name'],
            coefficient=data['coefficient'],
            subject_id=data.get('id'),
            created_at=created_at
        )
