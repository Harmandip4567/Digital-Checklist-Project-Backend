from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.config import settings
from app.database import get_db
from app import models
from sqlalchemy.orm import Session

def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def role_required(required_role: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Not authorized")
        return current_user
    return role_checker
