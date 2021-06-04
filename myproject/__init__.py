import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

#################################
######## DATABASE SETUP #########
#################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#################################
######### BLUEPRINTS ############
#################################
from myproject.core.views import cores_blueprint
from myproject.error_pages.handlers import error_pages_blueprint
from myproject.users.views import users_blueprint
from myproject.blogs.views import blogs_blueprint
from myproject.comments.views import comments_blueprint

app.register_blueprint(cores_blueprint)
app.register_blueprint(error_pages_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(blogs_blueprint)
app.register_blueprint(comments_blueprint)

login_manager.init_app(app)
login_manager.login_view = 'users.login'
