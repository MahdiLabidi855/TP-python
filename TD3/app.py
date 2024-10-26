import os
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequestKeyError
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from flask_mysqldb import MySQL

# Initialize Flask app
app = Flask(__name__)

# Secret key for session handling
app.config['SECRET_KEY'] = os.urandom(24)

# Configure MySQL Database for Flask-MySQLdb
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'user'  # Adjust password if needed
app.config['MYSQL_DB'] = 'flasktp1p1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:user@localhost/flasktp1p1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy, Babel, and MySQL
db = SQLAlchemy(app)
babel = Babel(app)
mysql = MySQL(app)

# Initialize Flask-Admin
admin = Admin(app, template_mode='bootstrap3')

# Configure Flask-Uploads
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image'
configure_uploads(app, photos)

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(255))
    is_active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_onupdate=db.func.now())

    def __str__(self):
        return self.username

# Admin view for User model
class UserAdmin(ModelView):
    column_exclude_list = ['password']

admin.add_view(UserAdmin(User, db.session))

# Allowed image types
def allowed_image(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Route to add a new user
@app.route('/addUser/', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        try:
            form = request.form
            name = form.get("username", "").strip()
            email = form.get("email", "").strip()
            pw = form.get("password", "").strip()
            photo = request.files.get("photo")

            # Validate that required fields are present
            if not (name and email and pw):
                flash('All fields (username, email, password) are required.', 'danger')
                return render_template('addUser.html')

            # Handle photo upload if provided
            photo_name = None
            if photo and allowed_image(photo.filename):
                filename = os.path.basename(photo.filename)  # Get safe filename
                photo_name = photos.save(photo, name=filename)
            elif photo:
                flash('Invalid photo format.', 'danger')
                return render_template('addUser.html')

            # Hash password
            hashed_pw = generate_password_hash(pw)

            # Insert user into MySQL database
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO user (username, email, password, photo) VALUES (%s, %s, %s, %s)",
                (name, email, hashed_pw, photo_name)
            )
            mysql.connection.commit()
            cur.close()

            flash('User successfully added.', 'success')
            return redirect(url_for('users'))

        except UploadNotAllowed:
            flash('File type not allowed.', 'danger')
        except BadRequestKeyError:
            flash('Missing required fields.', 'danger')
        except Exception as e:
            flash(f'Operation failed: {str(e)}', 'danger')

    return render_template('addUser.html')

# Route to display all users
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Run the Flask app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
