"""Routes
  Different URLs the app implements.
  Handlers for the app routes are written as Python functions, called view functions. These are mapped
  to one or more route URLs
  @ -> decorators
Returns:
"""
# Import render_template to call the htmls inside teh templates folder
# flash to show messages
# redirect to send to another web page
# url_for to generate URLs using an internal mapping of URLs to views functions.
# flask provides a request variables that contains all the information
# that the client sent with the request
from crypt import methods
from flask import render_template, flash, redirect, template_rendered, url_for, request
# We have to import current_user and login_user from flask-login
# logout_user to log out of the application
# login_required to protect functions to be accessed by not logged-in users
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
#from app import app and db
from app import app, db
#Import the classes from the forms module
from app.forms import LoginForm, RegistrationForm, EditProfileForm
# Import the class User from app/models.py
from app.models import User
# We need to use datetime in before_request()
from datetime import datetime

# decorator modifies the function that follows it
# creates an association between the route and the function
@app.route('/')
@app.route('/index')
# Flask-Login protects a view function against anonymous users with this decorator
# which redirects to the login page. But adding some extra information, a query 
# string argument to this URL making the redirect: /login?next=/index.
# Next query string argument is set to the original URL, so the app can use that
# to redirect back after login
@login_required
def index(): #1
    #return "Hello, World!" #1
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    # When we implement users we can remove user=user from here
    return render_template('index.html', title='Home Page', posts=posts)

# methods tells Flask that this view function accepts GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Before we can see the login form we need to codify the route
    and the function attached to it

    Returns:
        _type_: we return redirect or render_template
    """
    # We use the current_user imported before and one of those required properties
    # for flask-login implemented with UserMixin
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #Create an object form from the class LoginFrom
    form = LoginForm()
    # This method does all the form processing work.
    # Returns False if the browser sends the GET request to receive
    # the web page with the form.
    # If the browser send the POST request (press submit button), form.validate_on_submit
    # will gather all the data, run the validators attached to the fields and
    # if everything is ok return True. If this happens we call flash() function,
    # imported to show message to the user; and redirect(),
    # which instructs the client web browser to navigate to a different page.
    if form.validate_on_submit():
        # Return the first element of the search. Will only be 0 or 1
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # when we call flash, Flask stores the message, but we need to add functionality
            # in base.html to see these messages
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # If login and pass are correct then I call login_user function
        # coming from Flask-Login. This function register the user as logged in,
        # so any future pages the user navigate to will have the current_user
        # variable set to that user.
        login_user(user, remember=form.remember_me.data)
        """in a friendly dictionary format. Three cases.
        The request.args attribute exposes the contents of the query string
        Login URL doesn't have next argument -> user redirected to index page
        Login URL includes next arg. that is set to a relative path (URL
        without the domain portion), the users is redirected to that URL
        Login URL includes a next argument set to a full URL that includes a 
        domain name, the user is redirected to the index page."""
        next_page = request.args.get('next')
        # werkzeug url_parse function to check if url is relative or absolute.
        # and check if the netloc comp is true or false
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        #The message is created but not showed. We need to add code in base.html
        # flash(
        #     f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(next_page)
    """We can see login.html and we send arguments to it, title will be in base.html
    and form will be in login.html. We pass form object to the variable form"""
    return render_template('login.html', title='Sign In', form=form)

# This option is for the user to log out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# New user registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User profile page
# The decorator has a dynamic component <username>. Flask will accept any text
# in that portion of the URL
@app.route('/user/<username>')
# View only accesible to logged in users
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# Record time of last visit
@app.before_request
def before_request():
    if current_user.is_authenticated:
        # When we reference current_user, Flask-Login will invoke the user
        # loader callback function, which will run a db query that will put 
        # the target user in the db session. We don't need db.session.add()
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# Function that ties form and template together
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    # If validate on submit return True we copy the data from the form into the
    # user object and write the object to the db.
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    # If return false could be because the browser send a GET request
    # I need to respond by providing an initial version of the form template
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    # POST request with form data but something in the data is invalid
    return render_template('edit_profile.html', title='Edit Profile', form=form)
