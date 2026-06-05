from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse
)

from app.services.auth_service import AuthService
from app.dependencies.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    try:

        user = AuthService.register_user(
            db=db,
            full_name=user_data.full_name,
            email=user_data.email,
            password=user_data.password
        )

        return user

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    try:

        return AuthService.login(
            db=db,
            email=user_data.email,
            password=user_data.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )