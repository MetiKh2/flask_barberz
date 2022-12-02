from flask import Flask, render_template, request, redirect, url_for, flash, abort, __version__
from flask_login import current_user, login_required
from db_manager import db
from sqlalchemy import or_,desc
from models import Reserve,Service
from werkzeug.security import generate_password_hash
from validators.reserves import CreateReserveForm
from datetime import datetime

class Reserves:

    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def reserves_list(self):
        if not current_user.admin:
            abort(403)
        if request.method == 'POST':
            db.session.query(Reserve.Reserves).filter(
                Reserve.Reserves.id == int(request.args.get('id'))).delete()
            db.session.commit()
        reserves = db.session.query(Reserve.Reserves).order_by(desc(Reserve.Reserves.created_at)).all()
        return render_template('/admin/reserves/index.html', reserves=reserves)
    @login_required
    def cancel_reserve(self):
        if not current_user.admin:
            abort(403)
        id=request.args.get('id')
        reserve = db.session.query(Reserve.Reserves).filter(Reserve.Reserves.id==id).first()
        reserve.isCanceled=not reserve.isCanceled
        db.session.add(reserve)
        db.session.commit()
        return redirect(url_for('reserves_list'))

    @login_required
    def add_reserve(self):
        if not current_user.admin:
            abort(403)

        form = CreateReserveForm()
        services=db.session.query(Service.Services).all()
        choices=[]
        for choice in services:
            choices.append((choice.id,choice.title))
        form.services.choices=choices
        if request.method == 'POST':
            if form.validate():
                fullname = request.form['fullname']
                phone = request.form['phone']
                description = request.form['description']
                date = request.form['date']
                time = request.form['time']
                selected_services = request.form.getlist('services')
                new_reserve = Reserve.Reserves(
                    fullname=fullname, phone=phone, description=description,
                    date=datetime.strptime(date, '%Y-%m-%d'), time=time,
                    user_id=current_user.id)
                db.session.add(new_reserve)
                result = db.session.commit()
                for services in selected_services:
                    db.session.add(Reserve.ReserveServices(reserve_id=new_reserve.id,service_id=services))
                db.session.commit()
                if result != False:
                    flash('Reserve Created Succesfully', 'success')
                else:
                    flash('Error Server ,Please Try Again', 'danger')
        return render_template('/admin/reserves/create.html', form=form,services=services)

    @login_required
    def edit_reserve(self, reserve_id):
        if not current_user.admin:
            abort(403)
        form = CreateReserveForm()
        services=db.session.query(Service.Services).all()
        choices=[]
        for choice in services:
            choices.append((choice.id,choice.title))
        form.services.choices=choices
        reserve = db.session.query(Reserve.Reserves).filter(
            Reserve.Reserves.id == reserve_id).one()
        if not reserve:
            abort(404)
        if request.method == 'POST':
            if form.validate():
                fullname = request.form['fullname']
                phone = request.form['phone']
                description = request.form['description']
                date = request.form['date']
                time = request.form['time']
                selected_services = request.form.getlist('services')
                reserve.fullname =fullname
                reserve.phone = phone
                reserve.description = description
                reserve.time = time
                if date:
                    reserve.date = datetime.strptime(date, '%Y-%m-%d')
                db.session.add(reserve)
                db.session.query(Reserve.ReserveServices).filter(Reserve.ReserveServices.reserve_id==reserve_id).delete()
                for services in selected_services:
                    db.session.add(Reserve.ReserveServices(reserve_id=reserve.id,service_id=services))
                db.session.commit()
                return redirect(url_for('reserves_list'))
        return render_template('/admin/reserves/edit.html', services=services,form=form, reserve=reserve)
