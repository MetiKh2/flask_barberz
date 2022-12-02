from db_manager import db
from sqlalchemy import Integer, String, DateTime, Text, Column, Boolean, ForeignKey
from datetime import datetime
from models.User import Users
from models.Service import Services


class Reserves(db.Model):
    id = Column(Integer(), primary_key=True)
    fullname = Column(String(), nullable=False)
    phone = Column(String(), nullable=False)
    user_id = Column(Integer(), ForeignKey('users.id'))
    description = Column(Text())
    date = Column(DateTime(), nullable=False)
    time = Column(String(), nullable=False)
    isCanceled = Column(Boolean(), default=False)
    created_at = Column(DateTime(), default=datetime.now())

    def get_user(self):
        user = db.session.query(Users).filter(Users.id == self.user_id).first()
        return user.username

    def get_services(self):
        reserve_services = db.session.query(ReserveServices).filter(
            ReserveServices.reserve_id == self.id).with_entities(ReserveServices.service_id).all()
        print(reserve_services)
        print('------------------------')
        services = []
         
        for service_id in reserve_services:
            print(service_id[0])
            print('######################')
            
            services.append(db.session.query(Services).filter(
                Services.id == service_id[0]).with_entities(Services.title).first())
        return services


class ReserveServices(db.Model):
    id = Column(Integer(), primary_key=True)
    reserve_id = Column(Integer(), ForeignKey('reserves.id'))
    service_id = Column(Integer(), ForeignKey('services.id'))
