from flask import Flask
from flask_restful import Api
from resources.firebase import Firebase, FirebaseList

app = Flask(__name__)

app.config['DEBUG'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Firebase, '/firebase/<string:imsi>')
api.add_resource(FirebaseList, '/firebases')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    # app.run(port=5000)
    app.run(port=5000, host='0.0.0.0', threaded=True, debug=True)
