from typing import Optional
from ..models.user import User
from ..repositories.user_repository import UserRepository


class UserService:
    
    def __init__(self):
        self.repository = UserRepository()
        self.is_logged_in = False
        self.current_user: Optional[User] = None
    
    def register(self, username: str, password: str, role: str = "staff") -> Optional[User]:
        user = self.repository.create(username, password, role)
        return user
    
    def login(self, username: str, password: str) -> bool:
        user = self.repository.find_by_credentials(username, password)
        
        if user:
            self.is_logged_in = True
            self.current_user = user
            return True
        else:
            self.is_logged_in = False
            self.current_user = None
            return False
    
    def logout(self):
        self.is_logged_in = False
        self.current_user = None
    
    def me(self) -> Optional[User]:
        if self.is_logged_in:
            return self.current_user
        return None
