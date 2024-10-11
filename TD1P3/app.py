from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_mysqldb import MySQL
import yaml
from config import Config
from extensions import db
from resources.user import UserListResource

# Load YAML database configuration
db_config = yaml.safe_load(open('db.yaml'))

app = Flask(__name__)
app.config.from_object(Config)

# MySQL Configuration
app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)

def create_app():
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
    return "L'exécution est Postman pour tester les APIs"

@app.route("/users")
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM user")
    if resultValue > 0:
        users = cur.fetchall()
        return render_template('users.html', users=users)
    cur.close()
    return render_template('users.html', users=[])

@app.route("/addUser/", methods=["GET", "POST"])
def addUser():
    if request.method == "POST":
        form = request.form
        name = form["username"]
        email = form["email"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(username, email) VALUES(%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return render_template('addUser.html', message="User added successfully!")
    return render_template('addUser.html')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
