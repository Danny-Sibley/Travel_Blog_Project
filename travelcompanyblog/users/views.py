from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from travelcompanyblog import db 
from travelcompanyblog.models import User, BlogPost
from travelcompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from travelcompanyblog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

#register
@users.route('/register', methods =['GET', 'POST'] )
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        #if USer class passes checks of unique email and username
        try: 
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.login'))
        except: 
            flash('Registration Error: username or email already registered')
    return render_template('register.html', form = form)

#login
@users.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #grabs user from db based off provided email
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None: 
            if user.check_password(form.password.data):
                login_user(user)
                #stores page user was trying to access before logging in 
                next = request.args.get('next')
                
                if next ==None or not next[0] == '/':
                    next = url_for('core.blog')
                return redirect(next) 
            else:
                flash('Log in Unsuccessful: Incorrect Password')
        else:
            flash('Log in Unsuccessful: Email Not Registered')
        
    return render_template('login.html', form = form)
        
#logout 
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))
    
#account (update UserForm)
@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if request.method == 'POST':
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

            
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type= int)
    user = User.query.filter_by(username= username).first_or_404()
    #checks blog posts from the user, orders by date and shows 5 blog posts per page 
    blog_posts = BlogPost.query.filter_by(author = user).order_by(BlogPost.date.desc()).paginate(page = page, per_page=5)
    return render_template('user_blog_posts.html',blog_posts = blog_posts, user =user )
# user's list of Blog Posts
