from datetime import timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import json
from sqlalchemy.orm import Session

from auth.services.security import get_password_hash, pwd_context, create_access_token
from config.settings import settings
from users.repository.user_repository import UserRepository
from auth.services.validate_password import ValidatePassword
from auth.services.email_validator import EmailValidator


class AuthService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def login(self, form_data: OAuth2PasswordRequestForm = Depends()) :
        user = self.user_repository.get_user_by_email(form_data.username)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not pwd_context.verify(form_data.password, user.cPassword):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        json_data = json.dumps({"sub": str(user.uuid)})
        scope_roles = []
        if len(user.cRoles) > 0:
            for role in user.cRoles:
                scope_roles.append(role+":"+role)

        return {
            "access_token": create_access_token(
                data={"sub": str(user.uuid), "scopes":scope_roles},
            ),
            "token_type": "bearer",
        }
    
    #Funcion que retorna el current user

    


