from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import Utils
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

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user or not Utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Pass both username and role to JWT
    token = Utils.create_access_token({
    "sub": db_user.username,
    "role": db_user.role,
    "user_id": db_user.id
})
# during returning the keys we need to use the same returning parameters name as we define in the schema because this is way to check that only that key's  are returning that we define in response model schema
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role,
        "user_id": db_user.id
    }
