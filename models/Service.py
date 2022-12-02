from db_manager import db
from sqlalchemy import Integer,String,DateTime,Boolean,Column
from datetime import datetime

class Services(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    price = Column(Integer(),nullable=False)
    created_at = Column(DateTime(),default=datetime.now())