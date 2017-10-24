"""App is defined here"""
# pylint: disable=invalid-name
import traceback

from flask import jsonify
from flask_cors import CORS
import connexion

from todo.config import DEBUG, HOST
from todo.database import session, create_tables
from todo.exceptions import NotFoundError


def handle_general_exception(error):
    """Return response for general errors."""
    if DEBUG:
        traceback.print_exc()

    response = jsonify({'error': str(error), 'status': 500})
    response.status_code = 500
    return response


def handle_not_found_error(error):
    """Handle not found error"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app = connexion.FlaskApp(__name__, debug=DEBUG)
app.add_api('todo-api.yaml', arguments={'host': HOST})
app.add_error_handler(Exception, handle_general_exception)
app.add_error_handler(NotFoundError, handle_not_found_error)

application = app.app
CORS(application, origins=['http://localhost:3000'])


@application.teardown_appcontext
def remove_sessions(exception=None):  # pylint: disable=unused-argument
    """Remove session on teardown"""
    session.remove()


if __name__ == '__main__':
    create_tables()
    app.run(port=9090)
