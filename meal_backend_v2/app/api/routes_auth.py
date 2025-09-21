from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.security import Security

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_session)):
    auth = AuthService(db)
    user = auth.register_user(payload.first_name, payload.last_name, payload.email, payload.password)
    return {"message": "User created", "user_id": user.id}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_session)):
    auth = AuthService(db)
    user = auth.authenticate_user(payload.email, payload.password)
    token = Security.create_access_token({"user_id": user.id, "email": user.email})
    return TokenResponse(access_token=token)
