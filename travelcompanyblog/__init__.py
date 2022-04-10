from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from flask_ckeditor import CKEditor
#loads envirnoment variables 
load_dotenv()

app = Flask(__name__)
#add CKeditor   
ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
#########################
###### DATABASE SETUP####
#########################

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

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
from travelcompanyblog.blog_posts.views import blog_posts
#########################
###### Blueprinnts ######
#########################
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
