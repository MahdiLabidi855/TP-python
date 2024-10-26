from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_mysqldb import MySQL

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for CSRF protection

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'user'
app.config['MYSQL_DB'] = 'flasktp1p1'
mysql = MySQL(app)

# Define Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

# Route: Add User
@app.route("/addUser/", methods=["GET", "POST"])
def addUser():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.username.data
            email = form.email.data
            pw = generate_password_hash(form.password.data)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (name, pw, email))
            mysql.connection.commit()
            cur.close()

            flash('User successfully inserted.', 'success')
            return redirect(url_for('users'))
        else:
            flash('Form validation failed. Please check your inputs.', 'danger')
    return render_template('addUser.html', form=form)

# Route: List Users and Test Password Hash
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM user")
    users = cur.fetchall() if resultValue > 0 else []

    cur1 = mysql.connection.cursor()
    resultValue1 = cur1.execute("SELECT password FROM user WHERE username = 'admin3'")
    user = cur1.fetchone() if resultValue1 > 0 else None

    if user and check_password_hash(user['password'], 'admin'):
        flash(f"Correct password for {user['password']}", "success")
    else:
        flash("Incorrect password", "warning")

    cur.close()
    return render_template('users.html', users=users)

# Main Entry
if __name__ == "__main__":
    app.run(debug=True)
