from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from core.apis.assignments import (
    student_assignments_resources, 
    teacher_assignments_resources, 
    principal_assignments_resources
)

# Register blueprints with appropriate URL prefixes
app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')


@app.route('/')
def ready():
    """
    Health check endpoint to indicate service readiness.
    Returns the current UTC time for tracking purposes.
    """
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })
    return response


@app.errorhandler(Exception)
def handle_error(err):
    """
    Global error handler for catching and returning meaningful error responses.
    Handles various exception types including custom and library-specific errors.
    """
    # Handle custom application errors (FyleError)
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__,
            message=err.message
        ), err.status_code
    
    # Handle validation errors from Marshmallow
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__,
            message=err.messages
        ), 400
    
    # Handle database integrity errors (SQLAlchemy)
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__,
            message=str(err.orig)
        ), 400
    
    # Handle HTTP-specific exceptions
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__,
            message=str(err)
        ), err.code

    # Re-raise the error if it’s not handled
    raise err
