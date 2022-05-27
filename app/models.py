"""DB models
The data that will be stored in the DB will be represented by a collection
of classes (DB models). This defines the DB structure (schema) for this app.

Returns:
    _type_: _description_
"""
# We need to import daytime to use datetime.utcnow function
from datetime import datetime
from app import db, login

# Import the class UserMixin to implement is_authenticated, is_active,
# is_anonymous and get_id, which are the requirements for flask_login to work
from flask_login import UserMixin

# import functions from the package werkzeug to work with hash passwords
from werkzeug.security import generate_password_hash, check_password_hash

# To generate an avatar
from hashlib import md5

# Model representing users, inherits from db.Model, a base class for all models
# from Flask-SQLAlchemy. Fields are create as instances of the db.Column class which
# takes several arguments
# We add the class UserMixin to the User class.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # We will not be storing user passwords in the DB
    password_hash = db.Column(db.String(128))
    # The model is referenced by the model class Post.
    # posts field initialized by db.relationship.
    # Not an actual db field, but a high-level view of relationship between
    # users and posts.
    # For one to many relationships db.relationship field in normaly defined
    # on the "one" side.
    # The first argument represents the "many" side of the relationship
    # backref arg. defines the name of a field that will be added to the
    # objects of the "many" class that points back at the "one" object.
    # lazy argument define how the db query for the relationship will be issued.
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    # New fields. We will need to generate a database migration
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # __repr__ method tells Python how to print objects of this class.
    def __repr__(self):
        return "<User {}>".format(self.username)

    # method to generate a password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # function to check if the password inserted is correct or not
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


# The class Post represent blog posts written by users.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # We pass the function datetime.utcnow itself not the result of calling it
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # This field was inititialized as a foreign key to user.id. user is
    # the name of the database table for the model
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)


# The decorator register the user loader.
# The extension expects that the app will configure a user loader function,
# that can be callend to load a user given the ID
@login.user_loader
def load_user(id):
    # Flask-Login passes id to the function as a string. Databases that use
    # numeric IDs need to convert it to Int
    return User.query.get(int(id))
