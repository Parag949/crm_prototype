from flask import Blueprint, render_template, request, flash, redirect
from flask_login import current_user,login_required
views = Blueprint('views', __name__)

@views.route('/')#the function will run when the user goes to the root URL "/"
@login_required  # This decorator ensures that only logged-in users can access this route
def home():
    return render_template('home.html', title='Home', user=current_user)  # Render the home page template with the current user

