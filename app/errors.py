"""errors.py
  This module is to put all the error handlers together

Returns:
  html: custom error page
"""

from flask import render_template
from app import app, db

# This decorator is used to declare a custom error handler.
@app.errorhandler(404)
def not_found_error(error):
  # Return the template and the error code number. In the view functions I don't need to 
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('500.html'), 500