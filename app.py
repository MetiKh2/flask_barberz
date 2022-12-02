from flask import Flask, render_template
from sqlalchemy import desc
import os
from db_manager import db
from controllers import auth,reserve,home
from controllers.admin import admin,users,services,reserves
from models import User
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY')
if app.config['ENV']=='production' :
    app.config.from_object('config.ProductionConfig')
else :
    app.config.from_object('config.DevelopmentConfig')
login = LoginManager()
login.login_view = 'Login'
login.login_message_category = 'info'
login.init_app(app)


@login.user_loader
def userLoader(user_id):
    return db.session.query(User.Users).get(user_id)


db.init_app(app)
with app.app_context():
    db.create_all()

UPLOAD_DIR = os.path.curdir = 'static/uploads/'

app.secret_key = '1dae11441a1a2acf1cad3eca'
app.jinja_env.line_statement_prefix = '@'

authController=auth.Auth()
reserveController=reserve.Reserve()
homeController=home.Home()
adminController=admin.Admin()
usersController=users.Users()
servicesController=services.Services()
reservesController=reserves.Reserves()

app.add_url_rule('/', 'main', homeController.home,methods=['GET'])
app.add_url_rule('/comment', 'send_comment', homeController.send_comment,methods=['GET','POST'])


#auth
app.add_url_rule('/register', 'Register', authController.Register,methods=['GET',"POST"])
app.add_url_rule('/login', 'Login', authController.Login,methods=['GET',"POST"])
app.add_url_rule('/logout', 'Logout', authController.SignOut,methods=['GET',"POST"])

#reserve
app.add_url_rule('/reserve', 'Reserve', reserveController.Reserve,methods=['GET',"POST"])
app.add_url_rule('/reserves', 'reserves', reserveController.reserves,methods=['GET'])

#admin
app.add_url_rule('/admin', 'Admin', adminController.admin,methods=['GET'])
#comments
app.add_url_rule('/admin/comments', 'comments_list', adminController.comments_list,methods=['GET','POST'])
app.add_url_rule('/admin/comments/approve/<int:comment_id>/<string:status>', 'approve_comment', adminController.approve_comment,methods=['GET','POST'])
#users
app.add_url_rule('/admin/users', 'users_list', usersController.users_list,methods=['GET','POST'])
app.add_url_rule('/admin/users/create', 'add_user', usersController.add_user,methods=['GET','POST'])
app.add_url_rule('/admin/users/edit/<int:user_id>', 'edit_user', usersController.edit_user,methods=['GET','POST'])
#services
app.add_url_rule('/admin/services', 'services_list', servicesController.services_list,methods=['GET','POST'])
app.add_url_rule('/admin/services/create', 'add_service', servicesController.add_service,methods=['GET','POST'])
app.add_url_rule('/admin/services/edit/<int:service_id>', 'edit_service', servicesController.edit_service,methods=['GET','POST'])
#reserve
app.add_url_rule('/admin/reserves', 'reserves_list', reservesController.reserves_list,methods=['GET','POST'])
app.add_url_rule('/admin/reserves/create', 'add_reserve', reservesController.add_reserve,methods=['GET','POST'])
app.add_url_rule('/admin/reserves/edit/<int:reserve_id>', 'edit_reserve', reservesController.edit_reserve,methods=['GET','POST'])
app.add_url_rule('/admin/reserves/cancel', 'cancel_reserve', reservesController.cancel_reserve,methods=['GET','POST'])

@app.template_filter('showPrice')
def showPrice(price):
    return (f"{price:,}")

app.jinja_env.filters['showPrice'] = showPrice

if __name__ == '__main__':
    app.run(debug=True,port=2022)
