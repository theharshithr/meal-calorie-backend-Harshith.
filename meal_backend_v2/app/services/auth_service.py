from app.models.user import User
from app.core.security import Security
from sqlmodel import Session, select
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> User:
        q = select(User).where(User.email == email)
        existing = self.db.exec(q).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        hashed = Security.hash_password(password)
        user = User(first_name=first_name, last_name=last_name, email=email, password_hash=hashed)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> User:
        q = select(User).where(User.email == email)
        user = self.db.exec(q).first()
        if not user or not Security.verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user
