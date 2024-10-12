from sqlalchemy import Column, Integer, String, Boolean, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from config.db_config import engine
from datetime import datetime, timezone
import uuid, pytz


Base = declarative_base()


class Users(Base):
    __tablename__ = 'catUsers'
    fecha = datetime.utcnow() 
    fecha = fecha.astimezone( pytz.timezone('America/Mexico_City'))
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cNombre = Column(String(150))
    cApellido = Column(String(150))
    cEmail = Column(String(250), unique=True)
    cPassword = Column(String(250))
    dAlta = Column(DateTime, default=fecha)
    dBaja = Column(DateTime)
    dModificacion = Column(DateTime, default=fecha)
    bIsActive = Column(Boolean, default=True)
    cRoles = Column(ARRAY(String))


Base.metadata.create_all(engine)

