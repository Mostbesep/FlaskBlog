from app import db
from sqlalchemy import Column , Integer , String , Text

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(256), nullable=True, unique=False)
    slug = Column(String(128), nullable=False, unique=True)


class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, unique=True)
    summery = Column(String(256), nullable=True, unique=False)
    content = Column(Text, nullable=False, unique=False)
    slug = Column(String(128), nullable=False, unique=True)

