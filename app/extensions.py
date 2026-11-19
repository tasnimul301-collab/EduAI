"""Flask extensions module.

Instantiates extensions like SQLAlchemy without binding them
to a specific application instance yet. This prevents circular
import errors when using Flask Blueprints and models.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy ORM instance
db = SQLAlchemy()
