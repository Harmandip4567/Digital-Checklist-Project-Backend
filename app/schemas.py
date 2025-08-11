from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role:str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

class UserLogin(BaseModel):
    username: str
    password: str
    

class Token(BaseModel):
    user_id:int
    access_token: str
    token_type: str
    role: str

class ChecklistItemCreate(BaseModel):
    order: int
    label: str
    input_type: str
    required: bool = False
    frequency: Optional[str] = None
    unit: Optional[str] = None
    options: Optional[List[str]] = None

class ChecklistTemplateCreate(BaseModel):
    title: str
    description: Optional[str] = None
    created_by: Optional[int] = None
    steps: List[ChecklistItemCreate]

class ChecklistItemOut(BaseModel):
    id: int
    order: int
    label: str
    input_type: str
    required: bool
    frequency: Optional[str]
    unit: Optional[str]
    options: Optional[List[str]]

    class Config:
        from_attributes = True

class ChecklistTemplateOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_by: Optional[int]
    created_at: Optional[datetime]
    items: List[ChecklistItemOut] = []  # Means Iteams should be list and where each element is of type ChecklistItemOut

    class Config:
        from_attributes = True