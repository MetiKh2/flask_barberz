from flask import Flask, render_template, request, redirect, url_for, flash, abort, __version__
from flask_login import current_user, login_required
from db_manager import db
from sqlalchemy import or_
from models import User
from werkzeug.security import generate_password_hash
from validators.user import CreateUserForm,EditUserForm

class Users:

    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def users_list(self):
        if not current_user.admin:
            abort(403)
        if request.method == 'POST':
            db.session.query(User.Users).filter(
                User.Users.id == int(request.args.get('id'))).delete()
            db.session.commit()
        users = db.session.query(User.Users).all()
        return render_template('/admin/users/index.html', users=users)
    @login_required
    def add_user(self):
        if not current_user.admin:
            abort(403)

        form = CreateUserForm()
        if request.method == 'POST':
            if form.validate():
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                user = db.session.query(User.Users).filter(
                    or_(User.Users.email == email, User.Users.username == username)).first()
                if not user:
                    newUser = User.Users(
                        username=username, email=email, password=generate_password_hash(password))
                    db.session.add(newUser)
                    result = db.session.commit()
                    if result != False:
                        flash('User Created Succesfully', 'success')
                    else:
                        flash('Error Server ,Please Try Again', 'danger')
                else:
                    flash('User Exist', 'warning')
        return render_template('/admin/users/create.html', form=form)
    @login_required
    def edit_user(self,user_id):
        if not current_user.admin:
            abort(403)
        form = EditUserForm()
        user = db.session.query(User.Users).filter(
            User.Users.id == user_id).one()
        if not user:
            abort(404)
        if request.method == 'POST':
            if form.validate():
                username = request.form['username']
                email = request.form['email']
                admin = True if request.form.get('admin') =='on' else False
                other_user = db.session.query(User.Users).filter(
                    or_(User.Users.email == email, User.Users.username == username)).first()
                if not other_user or other_user.id == user.id:
                    user.username = username
                    user.email = email
                    user.admin = admin
                    db.session.add(user)
                    db.session.commit()
                else:
                    flash('Email or username is already exist', 'danger')
                    return redirect(url_for('edit_user'))
                return redirect(url_for('users_list'))
        return render_template('/admin/users/edit.html', form=form, user=user)