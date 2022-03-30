from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
#########################
###### DATABASE SETUP####
#########################

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/Travel_Blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#creates db and migrations 
db = SQLAlchemy(app)
Migrate(app,db)


#########################
###### LOGIN CONFIGS ####
#########################
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from travelcompanyblog.core.views import core
from travelcompanyblog.users.views import users 
from travelcompanyblog.error_pages.handlers import error_pages
#########################
###### Blueprinnts ######
#########################
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)