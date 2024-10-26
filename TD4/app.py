from flask import Flask, render_template, redirect, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

# Update the database URI to connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:user@localhost/flasktp1p1'  # Update with your MySQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to avoid warnings

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.username

# Function to load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In a real app, use hashed passwords
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Check password here (use hashing in real apps)
            login_user(user)
            flash(f'Welcome! {current_user.username}, you have been successfully logged in.', 'success')
            return redirect('/users')
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')

    return render_template('login.html')

@app.route('/users')
@login_required
def users():
    return render_template('users.html', username=current_user.username)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'info')
    return redirect('/')

# Create the database and tables
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
