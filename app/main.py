from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import signupLogin_auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Register routes
app.include_router(signupLogin_auth.router)

