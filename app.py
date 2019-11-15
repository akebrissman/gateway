from gateway import create_app
from gateway import db

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
app = create_app('flask.cfg')
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    print("in main")
    # app.run(port=5000)

    app.run(port=5000, host='0.0.0.0', debug=True)
