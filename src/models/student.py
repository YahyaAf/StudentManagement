from typing import Optional
from datetime import datetime, date


class Student:
    
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        date_of_birth: date,
        class_id: int,
        student_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self._id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._phone = phone
        self._date_of_birth = date_of_birth
        self._class_id = class_id
        self._created_at = created_at or datetime.now()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        if not value or len(value) < 2:
            raise ValueError("Le prenom doit contenir au moins 2 caracteres")
        self._first_name = value
    
    @property
    def last_name(self) -> str:
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str):
        if not value or len(value) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caracteres")
        self._last_name = value
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if not value or "@" not in value:
            raise ValueError("Email invalide")
        self._email = value
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, value: str):
        if not value:
            raise ValueError("Le telephone ne peut pas etre vide")
        self._phone = value
    
    @property
    def date_of_birth(self) -> date:
        return self._date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, value: date):
        if not value:
            raise ValueError("La date de naissance ne peut pas etre vide")
        self._date_of_birth = value
    
    @property
    def class_id(self) -> int:
        return self._class_id
    
    @class_id.setter
    def class_id(self, value: int):
        if not value:
            raise ValueError("Le class_id ne peut pas etre vide")
        self._class_id = value
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def __str__(self) -> str:
        return f"Student(id={self._id}, name='{self._first_name} {self._last_name}', email='{self._email}', class_id={self._class_id})"
    
    def __repr__(self) -> str:
        return (f"Student(student_id={self._id}, first_name='{self._first_name}', "
                f"last_name='{self._last_name}', email='{self._email}', phone='{self._phone}', "
                f"date_of_birth='{self._date_of_birth}', class_id={self._class_id}, created_at='{self._created_at}')")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Student):
            return False
        return self._id == other._id
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email,
            "phone": self._phone,
            "date_of_birth": self._date_of_birth.isoformat() if self._date_of_birth else None,
            "class_id": self._class_id,
            "created_at": self._created_at.isoformat() if self._created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        date_of_birth = None
        if data.get('date_of_birth'):
            if isinstance(data['date_of_birth'], str):
                date_of_birth = date.fromisoformat(data['date_of_birth'])
            else:
                date_of_birth = data['date_of_birth']
        
        created_at = None
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'])
            else:
                created_at = data['created_at']
        
        return cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            date_of_birth=date_of_birth,
            class_id=data['class_id'],
            student_id=data.get('id'),
            created_at=created_at
        )
