import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt import JWT
from dotenv import load_dotenv
import os

load_dotenv()


login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

#################################
######## DATABASE SETUP #########
#################################
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


##################################
############ API #################
#################################
from .api.secure_check import authenticate, identity

api = Api(app)
jwt = JWT(app, authenticate, identity)


#################################
######### BLUEPRINTS ############
#################################
from myproject.core.views import cores_blueprint
from myproject.error_pages.handlers import error_pages_blueprint
from myproject.users.views import users_blueprint
from myproject.blogs.views import blogs_blueprint
from myproject.comments.views import comments_blueprint
from myproject.mail.views import messages_blueprint

app.register_blueprint(cores_blueprint)
app.register_blueprint(error_pages_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(blogs_blueprint, url_prefix='/blogs')
app.register_blueprint(comments_blueprint, url_prefix='/comments')
app.register_blueprint(messages_blueprint, url_prefix='/mail')

login_manager.init_app(app)
login_manager.login_view = 'users.login'
