from werkzeug.security import generate_password_hash , check_password_hash
from sqlalchemy import Column , Integer , String
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer(),primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), unique=False, nullable=False)
    role = Column(Integer(), nullable=False, default=0)
    # if role = 0 => normal user
    # if role = 1 => admin user
    full_name = Column(String(128), nullable=True, unique=False)

    def set_password(self,password):
        self.password = generate_password_hash(password)


    def check_password(self,password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.role == 1