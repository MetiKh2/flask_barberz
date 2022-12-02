from flask import render_template, request, redirect, url_for, flash
from db_manager import db
from sqlalchemy import or_, and_,desc
from flask_login import current_user,login_required
from models import Reserve as ReserveModel,Service
from datetime import datetime
from validators.reserve import ReserveForm


class Reserve:
    def __init__(self, *args, **kwargs):
        pass
    
    @login_required
    def Reserve(self):
        now_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        services=db.session.query(Service.Services).all()
        form = ReserveForm()
        choices=[]
        for choice in services:
            choices.append((choice.id,choice.title))
        form.services.choices=choices
        if request.method == 'POST':
            if form.validate():
                fullname = request.form['fullname']
                phone = request.form['phone']
                description = request.form['description']
                selected_services = request.form.getlist('services')
                print(selected_services)
                date_time = request.form['datetime']
                date_time = date_time.split('T')
                new_reserve = ReserveModel.Reserves(fullname=fullname,
                                                    phone=phone, description=description,
                                                    date=datetime.strptime(
                                                        date_time[0], '%Y-%m-%d'),
                                                    time=date_time[1],
                                                    user_id=current_user.id)
                db.session.add(new_reserve)
                db.session.commit()
                for services in selected_services:
                    db.session.add(ReserveModel.ReserveServices(reserve_id=new_reserve.id,service_id=services))
                db.session.commit()
                flash('رزرو شما ثبت شد','success')
               #  print(datetime.strptime(date_time[0],'%Y-%m-%d'))
        return render_template('reserve.html', now_date=now_date, form=form,services=services)

    @login_required
    def reserves(self):
        reserves = db.session.query(ReserveModel.Reserves).filter(ReserveModel.Reserves.user_id==current_user.id).order_by(desc(ReserveModel.Reserves.created_at)).all()
        return render_template('reserves.html', reserves=reserves)
