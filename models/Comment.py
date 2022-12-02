from db_manager import db
from sqlalchemy import Integer,Text,DateTime,ForeignKey,Column,Boolean
from datetime import datetime
from models.User import Users
class Comments(db.Model):
    id = Column(Integer(), primary_key=True)
    text = Column(Text(), nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'))
    created_at = Column(DateTime(),default=datetime.now())
    published= Column(Boolean(), default=False)
    
    def get_writer(self):
        user=db.session.query(Users).filter(Users.id==self.user_id).first()
        return user.username