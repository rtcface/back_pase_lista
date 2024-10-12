from enum import Enum

from pydantic import BaseModel, Field, UUID4, EmailStr
from typing import Optional
from datetime import datetime

class Roles(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"

class UserBase(BaseModel):
    cNombre: str = Field(min_length=2, max_length=150)
    cApellido: str = Field(min_length=2, max_length=150)
    cEmail: EmailStr = Field(min_length=2, max_length=254)
    cRoles: Optional[list[Roles]] = Field(default=[Roles.USER])


class AddUserInput(UserBase):
    cPassword: str = Field(min_length=8, max_length=120)

class UserOutput(UserBase):
    uuid: UUID4 = Field(..., alias="id")
    bIsActive: bool
    dFechaRegistro: datetime
    dFechaModificacion: datetime
    dFechaBaja: Optional[datetime]=None
    

class UserValidaLogin(UserOutput):
    cPassword: str = Field(..., alias="password")

class UpdateUserInput(UserBase):
    uuid: UUID4 = Field(..., alias="uuid")

class DeleteUserInput(BaseModel):
    uuid: UUID4 = Field(..., description="The user's UUID")


class TokenData(BaseModel):
    uuid: Optional[str] = None
    scopes: list[str] = []


class GetUserByUuid(TokenData):
    uuid: Optional[str] = None

class TokenOutput(BaseModel):
    access_token: str
    token_type: str

