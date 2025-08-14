from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import signupLogin_auth
from app.routes import users
from app.routes import Checklist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vite's default development port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(signupLogin_auth.router)
app.include_router(users.router)
app.include_router(Checklist.router)

