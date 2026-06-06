from fastapi import FastAPI

from app.models.user import User
from app.models.skill import Skill
from app.models.user_skill import UserSkill
from app.models.base import Base
from app.core.database import engine

from app.api.v1.auth import router as auth_router

app = FastAPI(
    title="CodeDNA API",
    version="1.0.0"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():

    return {
        "message": "Welcome to CodeDNA API!"
    }