from flask import Flask
from flask_migrate import Migrate
#Flask-Migrate is an extension that configures Alembic
# (tool which can handle the database migrations.)
#in the proper way to work with your Flask and Flask-SQLAlchemy application
from flask_restful import Api
# Flask-RESTful is an extension for Flask that adds support for quickly building
# REST APIs.
# A RESTful API is an architectural style for an application program interface
# (API) that
# uses HTTP requests to access and use data. That data can be used to
# GET, PUT, POST and DELETE data types, which refers
# to the reading, updating, creating and deleting of operations concerning
# resources.
from flask import Flask, request
from config import Config
from extensions import db
from resources.user import UserListResource
app = Flask(__name__)
def create_app():
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app
def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
def register_resources(app):
    api = Api(app)
    api.add_resource(UserListResource, '/users')
@app.route('/')
def home():
    return ('L\'execution est Postman pour tester les Apis ')
if __name__ == '__main__':
    app = create_app()
app.run()