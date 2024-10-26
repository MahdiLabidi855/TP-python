from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from flask_babel import Babel
import MySQLdb


# Génération d'une clé secrète pour les sessions
secret_key = os.urandom(24)

# Initialisation de Flask
app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:user@localhost/flasktp1p1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Initialisation de Babel
babel = Babel(app)

# Initialisation de Flask-Admin
admin = Admin(app, template_mode='bootstrap3')

# Modèle User
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(10024))

    def __str__(self):
        return self.username

# Vue d'administration pour User
class UserAdmin(ModelView):
    column_exclude_list = ['password']

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password =form.password.data #generate_password_hash(form.password.data)

admin.add_view(UserAdmin(User, db.session))

# Formulaire User
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

# Modèle Order
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="orders")

User.orders = db.relationship("Order", back_populates="user")

# Vue d'administration pour Order
class OrdersAdmin(ModelView):
    form_columns = ["order_date", "user"]
    column_list = ["order_date", "user"]

admin.add_view(OrdersAdmin(Order, db.session))

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
