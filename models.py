from Database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
import uuid

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)

class Wishes(Base):
    __tablename__ = 'wishes'

    id = Column(Integer, primary_key=True, index=True)
    wish_uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    birthday_person_name = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
