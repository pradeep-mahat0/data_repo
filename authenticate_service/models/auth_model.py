from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from authenticate_service.dependencies.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(100), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    manager_id = Column(String(100), nullable=True)
    manager_name = Column(String(255), nullable=True)
    status = Column(String(50), default="active")
    profile_pic = Column(String(500), nullable=True)
    external_email = Column(String(255), nullable=True)
    program_name = Column(String(255), nullable=True)
    
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

