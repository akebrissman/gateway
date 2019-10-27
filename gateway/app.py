from . import create_app
from . import db

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
app = create_app('flask.cfg')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    # app.run(port=5000)
    app.run(port=5000, host='0.0.0.0', threaded=True, debug=True)
