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
    order: int                  # this value is automatically getting from table so user does not need to provide this value 
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
    frequency: Optional[str]   # later i will change this name "frequency" to "value"
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
    items: List[ChecklistItemOut] = []  # normaly the the data object comes from frontend automatically converts to python List and goes to backend directly as  Here the combination of both the template and items data comes in the form of list so here we  put the template data directly and the items data is goes through the
    status: Optional[str] = None
    class Config:
        from_attributes = True

# schemas for editing both the template and items

class TemplateItemUpdate(BaseModel):
    id: Optional[int]   # may be None for new items
    label: str
    input_type: str
    required: bool
    frequency: Optional[str] = None
    unit: Optional[str] = None

    class Config:
        from_attributes = True

class TemplateUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    items: List[TemplateItemUpdate]

class AddNewChecklistItem(BaseModel):
    label: str
    input_type: str
    required: bool = False
    frequency: Optional[str] = None
    unit: Optional[str] = None
    options: Optional[List[str]] = None