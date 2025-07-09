from flask import Blueprint, render_template, request, flash, redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User  # Import the User model from models.py
from . import db  # Import the database instance from __init__.py
from flask_login import login_user, logout_user, current_user,login_required
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): #hash password and check it against user.password
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)# remember=True will keep the user logged in even after closing the browser
                #login_user is a function from flask_login that logs in the user and sets the session
                return redirect(url_for('views.home'))
            else:
                flash("Invalid email or password.", category='error')
        else:
            flash("User does not exist.", category='error')

    return render_template('login.html', title='Login',user=current_user)  # Render the login page template with the current user

@auth.route("/logout")
@login_required  # This decorator ensures that only logged-in users can access this route
def logout():
    logout_user()  # This will log out the current user
    flash("Logged out successfully!", category='success')
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method=="POST":
        email = request.form.get('email')
        first_name=request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists.", category='error')
        elif len(email)<4:
            flash("Email must be greater than 3 characters.", category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='scrypt')
            )
            db.session.add(new_user)
            db.session.commit()  # Commit the new user to the database #we need to commit the changes to the database to save the new user
            flash("Account Created Successfully", category='success')
            return redirect(url_for('views.home'))  # Redirect to the home page after successful sign-up
            #add user to database

    return render_template('sign-up.html', title='Sign Up',user=current_user)  # Render the sign-up page template with the current user