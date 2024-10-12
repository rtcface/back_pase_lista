from typing import Annotated

from fastapi import APIRouter, Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from sqlalchemy.orm import Session


from auth.services.auth import get_current_active_user
from config.db_config import get_db
from auth.services.auth_service import AuthService
from users.schemas.users_schema import UserOutput

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login", status_code=201)
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    _auth_service = AuthService(db)
    return _auth_service.login(data)

@router.get("/current_user", status_code=200, response_model=UserOutput)
async def get_current_user(current_user:Annotated[ UserOutput, Security(get_current_active_user)]):
    _auth_service = AuthService(get_db())
    return current_user

