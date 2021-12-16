from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
db = SQLAlchemy()


######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_endpoints(app)
    return app


##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)


def register_endpoints(app):
    # Since the application instance is now created, register each Endpoint
    # with the Flask application instance (app)
    from gateway.resources.firebase import Firebase, FirebaseId
    from gateway.resources.group import Group, GroupId
    from gateway.resources.device import Device, DeviceId
    api = Api(app)
    api.add_resource(FirebaseId, '/api/firebase/<string:imsi>')
    api.add_resource(Firebase, '/api/firebase')
    api.add_resource(GroupId, '/api/group/<string:group_name>')
    api.add_resource(Group, '/api/group')
    api.add_resource(DeviceId, '/api/device/<string:device_name>')
    api.add_resource(Device, '/api/device')
