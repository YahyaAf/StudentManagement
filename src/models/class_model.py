from typing import Optional
from datetime import datetime


class Class:
    
    def __init__(
        self,
        name: str,
        level: str,
        year: str,
        class_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self._id = class_id
        self._name = name
        self._level = level
        self._year = year
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
    def level(self) -> str:
        return self._level
    
    @level.setter
    def level(self, value: str):
        if not value:
            raise ValueError("Le level ne peut pas etre vide")
        self._level = value
    
    @property
    def year(self) -> str:
        return self._year
    
    @year.setter
    def year(self, value: str):
        if not value:
            raise ValueError("L'annee ne peut pas etre vide")
        self._year = value
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def __str__(self) -> str:
        return f"Class(id={self._id}, name='{self._name}', level='{self._level}', year='{self._year}')"
    
    def __repr__(self) -> str:
        return (f"Class(class_id={self._id}, name='{self._name}', "
                f"level='{self._level}', year='{self._year}', created_at='{self._created_at}')")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Class):
            return False
        return self._id == other._id
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "level": self._level,
            "year": self._year,
            "created_at": self._created_at.isoformat() if self._created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Class':
        created_at = None
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'])
            else:
                created_at = data['created_at']
        
        return cls(
            name=data['name'],
            level=data['level'],
            year=data['year'],
            class_id=data.get('id'),
            created_at=created_at
        )
