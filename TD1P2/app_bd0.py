from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from models.forms import UserForm  # Make sure you have this file
import os

# Generate a random secret key
secret_key = os.urandom(24)
app = Flask(__name__)
Bootstrap(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:user@localhost/flasktp1p1'
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200))

# Create tables in the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Utilisateur existe déjà.', 'warning')
        else:
            # Add the user to the database
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Utilisateur inséré correctement.', 'success')
    return render_template('index_bd01.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
