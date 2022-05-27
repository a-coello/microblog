# From app import app from app package import app and db variables
# both created in __init__.py
from app import app, db
# From models.py import User and Post class
from app.models import User, Post

# Creates the shell context that adds the database instance and models
# to the shell extension. We use "flask shell"
# The decorator registers the function as a shell context function.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
