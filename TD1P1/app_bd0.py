from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:user@localhost/flasktp1p1'
db = SQLAlchemy(app)

with app.app_context():
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), nullable=False, unique=False)
        email = db.Column(db.String(200), nullable=False, unique=True)
        password = db.Column(db.String(200))

    class Customer(db.Model):
        __tablename__ = 'customer'
        id = db.Column(db.Integer, primary_key=True)
        cname = db.Column(db.String(80), nullable=False)
        csurname = db.Column(db.String(80), nullable=False)
        cadr = db.Column(db.String(200))
        ctel = db.Column(db.String(15))

    class Product(db.Model):
        __tablename__ = 'product'
        id = db.Column(db.Integer, primary_key=True)
        lib = db.Column(db.String(80), nullable=False)
        up = db.Column(db.Float, nullable=False)
        qtes = db.Column(db.Integer, nullable=False)

    db.create_all()

@app.route('/')
def home():
    new_user = User(username='name15', email='name15@gmail.com', password='name15')
    try:
        if User.query.filter_by(username=new_user.username).first():
            return f"L'utilisateur existe déjà: {new_user.username}"
        elif User.query.filter_by(email=new_user.email).first():
            return f"L'email existe déjà: {new_user.email}"
        else:
            db.session.add(new_user)
            db.session.commit()
    except Exception as e:
        return str(e)
    
    return "L'exécution s'est bien déroulée"

if __name__ == '__main__':
    app.run(debug=True)
