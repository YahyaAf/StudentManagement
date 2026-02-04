from datetime import datetime
from typing import Optional


class User:
    
    def __init__(self, username: str, password: str, role: str = "staff", 
                 user_id: Optional[int] = None, created_at: Optional[datetime] = None):
        self._id = user_id
        self._username = username
        self._password = password
        self._role = role
        self._created_at = created_at if created_at else datetime.now()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def role(self) -> str:
        return self._role
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @username.setter
    def username(self, value: str):
        if not value or len(value) < 3:
            raise ValueError("Le nom d'utilisateur doit contenir au moins 3 caractères")
        self._username = value
    
    @password.setter
    def password(self, value: str):
        if not value:
            raise ValueError("Le mot de passe ne peut pas être vide")
        self._password = value
    
    @role.setter
    def role(self, value: str):
        allowed_roles = ["admin", "staff"]
        if value not in allowed_roles:
            raise ValueError(f"Rôle invalide. Rôles autorisés: {allowed_roles}")
        self._role = value
    
    def __str__(self) -> str:
        return f"User(id={self._id}, username='{self._username}', role='{self._role}')"
    
    def __repr__(self) -> str:
        return (f"User(user_id={self._id}, username='{self._username}', "
                f"role='{self._role}', created_at='{self._created_at}')")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self._id == other._id and self._username == other._username
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "username": self._username,
            "password": self._password,
            "role": self._role,
            "created_at": self._created_at.isoformat() if self._created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        created_at = None
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'])
            else:
                created_at = data['created_at']
        
        return cls(
            username=data['username'],
            password=data['password'],
            role=data.get('role', 'staff'),
            user_id=data.get('id'),
            created_at=created_at
        )
