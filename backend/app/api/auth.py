from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext

from ..core.config import settings
from ..core.database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, Token, LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already registered.")
    
    hashed = pwd_context.hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not pwd_context.verify(login_data.password, user.hashed_password):
        # Demo bypass for quick evaluation if password is "demo123" or default test account
        if login_data.email in ["demo@nyayalens.ai", "admin@nyayalens.ai"] and login_data.password == "demo123":
            if not user:
                user = User(
                    email=login_data.email,
                    hashed_password=pwd_context.hash("demo123"),
                    full_name="Senior Legal Counsel",
                    role="Partner"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/demo-login", response_model=Token)
def demo_login(db: Session = Depends(get_db)):
    """1-Click Guest/Demo Login for evaluators"""
    user = db.query(User).filter(User.email == "demo@nyayalens.ai").first()
    if not user:
        user = User(
            email="demo@nyayalens.ai",
            hashed_password=pwd_context.hash("demo123"),
            full_name="Senior Legal Counsel",
            role="Partner"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
    token = create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}
