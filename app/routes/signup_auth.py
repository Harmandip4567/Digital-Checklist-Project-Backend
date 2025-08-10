from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import Utils
from app import models, schemas, database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check email uniqueness
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check username uniqueness
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = Utils.hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw ,role=user.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
