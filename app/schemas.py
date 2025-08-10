from pydantic import BaseModel, EmailStr

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