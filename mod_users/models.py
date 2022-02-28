from sqlalchemy import Column , Integer , String
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer(),primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), unique=False, nullable=False)
    role = Column(Integer(), nullable=False, default=0)
    full_name = Column(String(128), nullable=True, unique=False)