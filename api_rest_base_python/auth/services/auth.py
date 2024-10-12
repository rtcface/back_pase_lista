from typing import Annotated


from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config.db_config import get_db
from users.models.users_model import Users
from users.schemas.users_schema import TokenData, UserOutput
from config.settings import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={"SUPER_ADMIN": "SUPER_ADMIN", "ADMIN":"ADMIN","USER": "USER" })

def get_user(db: Session, uuid: str):
    return db.query(Users).filter(Users.uuid == uuid).first()

async def get_current_user(security_scopes: SecurityScopes,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOutput:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        uuid: str = payload.get("sub")
        if uuid is None:
            print("uuid is None first")
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(uuid=uuid, scopes=token_scopes)
    except JWTError:
        raise credentials_exception
    user = get_user(db, uuid=uuid)
    if user is None:
        print("user is None")
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return UserOutput(
        id=user.uuid,
        cNombre=user.cNombre,
        cApellido=user.cApellido,
        cEmail=user.cEmail,
        bIsActive=user.bIsActive,
        dFechaRegistro=user.dAlta,
        dFechaModificacion=user.dModificacion,
        dFechaBaja=user.dBaja if user.dBaja is not None else None,
        cRoles=user.cRoles,
    )


async def get_current_active_user(current_user: UserOutput = Depends(get_current_user)):
    if not current_user.bIsActive:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
