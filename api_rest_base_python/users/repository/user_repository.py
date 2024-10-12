from sqlalchemy.orm import Session
from fastapi import HTTPException

from sqlalchemy import and_
from users.models.users_model import Users 
from users.schemas.users_schema import ( 
        AddUserInput,
        UserOutput,
        UpdateUserInput,
        DeleteUserInput,
        UserValidaLogin,
        GetUserByUuid,
        Roles
    )
from typing import List, Optional, Type
from pydantic import ValidationError, UUID4
from datetime import datetime, timezone
import pytz

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: AddUserInput) -> UserOutput:
        try:
            new_user = Users(
                cNombre=user.cNombre,
                cApellido=user.cApellido,
                cEmail=user.cEmail,
                cPassword=user.cPassword,
                cRoles = user.cRoles

            )
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return UserOutput(
                id=new_user.uuid,
                cNombre=new_user.cNombre,
                cApellido=new_user.cApellido,
                cEmail=new_user.cEmail,
                bIsActive=new_user.bIsActive,
                dFechaRegistro=new_user.dAlta,
                dFechaModificacion=new_user.dModificacion,
                dFechaBaja=new_user.dBaja if new_user.dBaja is not None else None,
                cRoles=new_user.cRoles

            )
        except Exception as e:
            self.session.rollback()
            return None
    def user_exists_by_email(self, email: str) -> bool:
        try:
            user = self.session.query(Users).filter(Users.cEmail == email).first()
            if user is None:
                return False
            return True
        except Exception as e:
            return False

    def get(self, uuid: UUID4) -> UserOutput:
        try:
            user = self.session.query(Users).filter(Users.uuid == uuid).first()
            if user is None:
                return None
            return UserOutput(
                id=user.uuid,
                cNombre=user.cNombre,
                cApellido=user.cApellido,
                cEmail=user.cEmail,
                bIsActive=user.bIsActive,
                dFechaRegistro=user.dAlta,
                dFechaModificacion=user.dModificacion,
                dFechaBaja=user.dBaja if user.dBaja is not None else None,
                cRoles=user.cRoles

            )
        except Exception as e:
            return None

    def get_user_by_email(self, email: str) -> UserValidaLogin:
        return self.session.query(Users).filter(and_(Users.cEmail == email)).first()
        
    def update(self, user_input: UpdateUserInput) -> UserOutput:
        try:
            fecha = datetime.utcnow()
            fecha = fecha.astimezone( pytz.timezone('America/Mexico_City'))

            user = self.session.query(Users).filter(Users.uuid == user_input.uuid).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            user.cNombre = user_input.cNombre if user_input.cNombre is not None else user.cNombre
            user.cApellido = user_input.cApellido if user_input.cApellido is not None else user.cApellido
            user.cEmail = user_input.cEmail if user_input.cEmail is not None else user.cEmail
            user.dModificacion = fecha
            user.cRoles = user_input.cRoles if user_input.cRoles is not None else user.cRoles
            self.session.commit()
            self.session.refresh(user)
            return UserOutput(
                id=user.uuid,
                cNombre=user.cNombre,
                cApellido=user.cApellido,
                cEmail=user.cEmail,
                bIsActive=user.bIsActive,
                dFechaRegistro=user.dAlta,
                dFechaModificacion=user.dModificacion,
                dFechaBaja=user.dBaja if user.dBaja is not None else None,
                cRoles=user.cRoles
            )
        except Exception as e:
            self.session.rollback()
            raise e
    # Funcion para desactivar el usuario
    def disable(self, uuid: UUID4) -> UserOutput:
        try:
            fecha = datetime.utcnow()
            fecha = fecha.astimezone( pytz.timezone('America/Mexico_City'))
            user = self.session.query(Users).filter(Users.uuid == uuid).first()
            if user is None:
                raise ValueError(f"User with UUID {uuid} not found")
            user.bIsActive = False
            user.dModificacion = fecha
            user.dBaja = fecha
            self.session.commit()
            self.session.refresh(user)
            return UserOutput(
                id=user.uuid,
                cNombre=user.cNombre,
                cApellido=user.cApellido,
                cEmail=user.cEmail,
                bIsActive=user.bIsActive,
                dFechaRegistro=user.dAlta,
                dFechaModificacion=user.dModificacion,
                dFechaBaja=user.dBaja if user.dBaja is not None else None,
                cRoles=user.cRoles
            )
        except Exception as e:
            self.session.rollback()
            raise e
    # Funcion para reactivar el usuario
    def enable(self, uuid: UUID4) -> UserOutput:
        try:
            fecha = datetime.utcnow()
            fecha = fecha.astimezone( pytz.timezone('America/Mexico_City'))
            user = self.session.query(Users).filter(Users.uuid == uuid).first()
            if user is None:
                raise ValueError(f"User with UUID {uuid} not found")
            user.bIsActive = True
            user.dModificacion = fecha
            self.session.commit()
            self.session.refresh(user)
            return UserOutput(
                id=user.uuid,
                cNombre=user.cNombre,
                cApellido=user.cApellido,
                cEmail=user.cEmail,
                bIsActive=user.bIsActive,
                dFechaRegistro=user.dAlta,
                dFechaModificacion=user.dModificacion,
                dFechaBaja=user.dBaja if user.dBaja is not None else None,
                cRoles=user.cRoles

            )
        except Exception as e:
            self.session.rollback()
            raise e
    
    def delete(self, uuid: UUID4) -> None:
        try:
            user = self.session.query(Users).filter(Users.uuid == uuid).first()
            if user is None:
                raise ValueError(f"User with UUID {uuid} not found")
            self.session.delete(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_all(self) -> List[UserOutput]:
        try:
            users = self.session.query(Users).all()
            return [UserOutput(
                id=user.uuid,
                cNombre=user.cNombre,
                cApellido=user.cApellido,
                cEmail=user.cEmail,
                bIsActive=user.bIsActive,
                dFechaRegistro=user.dAlta,
                dFechaModificacion=user.dModificacion,
                dFechaBaja=user.dBaja if user.dBaja is not None else None,
                cRoles=user.cRoles
            ) for user in users]
        except Exception as e:
            raise e
