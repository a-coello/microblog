
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''Flask and other extensions use the secret key as a
    cryptographic key, useful to generate signatures or tokens
    Flask-WTF ext uses it to protect web form against
    CSRF attacks
    '''

    # Value or hardcode string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Flask-SQLAlchemy extension takes the location of the application's DB from 
    # this SQLALCHEMY_DATABASE_URI variable. We take DB URL from the DATABASE_URL
    # environment variable and if it's not defined, a route to app.db in basedir
    # which is the main directory of the app
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # We put this to false because we don't need it now. It's to signal the app
    # every time a change is about to be made in the DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add email server details to this configuration file
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['alexcoeari73@gmail.com']
