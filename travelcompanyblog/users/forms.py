from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from travelcompanyblog.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    username = StringField('Username',validators = [DataRequired()])      
    password = PasswordField('Password',validators = [DataRequired(), EqualTo('pass_confirm',message = 'Passwords must match' )]) 
    #checks hashed password with stored hash password  
    pass_confirm = PasswordField('Confirm Pasword', validators = [DataRequired()])  
    submit = SubmitField('Register')
    
    
    #checks to see if email is already registered
    def check_email(self,field):
        if User.query.filter_by(email = field.data).first():   
            raise ValidationError ('Your email has been registered already!')
    
    #checks to see if username is already registered    
    def check_username(self,field):
        if User.query.filter_by(username = field.data).first():   
            raise ValidationError ('Your username has been registered already!')
        
class UpdateUserForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    username = StringField('UserName',validators = [DataRequired()])      
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    #checks to see if email is already registered
    def check_email(self,field):
        if User.query.filter_by(email = field.data).first():   
            raise ValidationError ('Your email has been registered already!')
    
    #checks to see if username is already registered    
    def check_username(self,field):
        if User.query.filter_by(username = field.data).first():   
            raise ValidationError ('Your username has been registered already!')