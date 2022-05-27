'''
A subdirectory including a __init__.py file is 
considered a package and can be imported.
__init__.py executes and defines what symbols the package
exposes to the outside world.
app package will host the application'''


from flask import Flask
# Import SQLAlchemy and Migrate to work with the DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Import Login manager from flask_login extension which manages the user logged-in state
# with this the app remembers if the user is logged in. Also provides a "remember me"
# functionality that allows users to remain logged in even after clossing the browser
# window
from flask_login import LoginManager
# Import class Config from module config
from config import Config
# Flask uses python's logging package to write its logs and send the logs by email
import logging
# To send out error I add SMTPHandler instance to the Flask logger object, which 
# is app.logger
from logging.handlers import SMTPHandler


app = Flask(__name__) #1 app here is an instance of the class Flask
#Tell Flask to read and apply the config file
app.config.from_object(Config)
# Create and instance of the DB Class and the Migrate Class
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Initialize the LoginManager after the app instance. Flask-Login needs to know what
# is the view function that handles logins
login = LoginManager(app)
# 'login' is the function or endpoint name for the login view, the name
# we would use in a url_for() call to get the URL
login.login_view = 'login'

# To send out errors
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


# It's done here to avoid circular imports
# Routes is a py module inside app folder (package). Here to avoid circular imports
# models.py is where we create the DB logic
# errors.py is where we handle errors
from app import routes, models, errors