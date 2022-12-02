from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Users(db.Model,UserMixin):
    id = Column(Integer(), primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    email = Column(String(),unique=True)
    password = Column(String(),nullable=False)
    admin = Column(Boolean(),default=False)
    phone = Column(String(),default='0')
    created_at = Column(DateTime(),default=datetime.now())
    token=Column(String(),default='')

    @property
    def passwd(self):
        raise AttributeError('Access Forbidden')
    
    @passwd.setter
    def passwd(self , password):
        self.password = generate_password_hash(password)
    
    def IsOriginalPassword(self , user_password):
        return check_password_hash(self.password , user_password)