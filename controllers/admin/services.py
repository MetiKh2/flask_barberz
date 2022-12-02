from flask import Flask, render_template, request, redirect, url_for, flash, abort, __version__
from flask_login import current_user, login_required
from db_manager import db
from sqlalchemy import or_
from models import User, Service
from werkzeug.security import generate_password_hash
from validators.user import CreateUserForm, EditUserForm
from validators.service import CreateServiceForm, EditServiceForm


class Services:

    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def services_list(self):
        if not current_user.admin:
            abort(403)
        if request.method == 'POST':
            db.session.query(Service.Services).filter(
                Service.Services.id == int(request.args.get('id'))).delete()
            db.session.commit()
        services = db.session.query(Service.Services).all()
        return render_template('/admin/services/index.html', services=services)

    @login_required
    def add_service(self):
        if not current_user.admin:
            abort(403)

        form = CreateServiceForm()
        if request.method == 'POST':
            if form.validate():
                title = request.form['title']
                price = request.form['price']
                newService = Service.Services(
                    title=title, price=price)
                db.session.add(newService)
                result = db.session.commit()
                if result != False:
                    flash('Service Created Succesfully', 'success')
                else:
                    flash('Error Server ,Please Try Again', 'danger')
        return render_template('/admin/services/create.html', form=form)

    @login_required
    def edit_service(self, service_id):
        if not current_user.admin:
            abort(403)
        form = EditServiceForm()
        service = db.session.query(Service.Services).filter(
            Service.Services.id == service_id).one()
        if not service:
            abort(404)
        if request.method == 'POST':
            if form.validate():
                title = request.form['title']
                price = request.form['price']
                service.title = title
                service.price = price
                db.session.add(service)
                db.session.commit()
                return redirect(url_for('services_list'))
        return render_template('/admin/services/edit.html', form=form, service=service)
