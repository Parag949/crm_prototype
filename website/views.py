from flask import Blueprint, jsonify, render_template, request, flash, redirect,url_for
from flask_login import current_user,login_required
views = Blueprint('views', __name__)
from .models import Note , Customer # Import the Note model from models.py
from . import db
import json

@views.route('/',methods=["GET","POST"])#the function will run when the user goes to the root URL "/"
@login_required  # This decorator ensures that only logged-in users can access this route
def home():
    if request.method == "POST":
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short!", category='error')  # Flash an error message if the note is too short
        elif len(note) > 1000:
            flash("Note is too long!", category='error')  # Flash an error message if the note is too long
        else:
            flash("Note added successfully!", category='success')  # Flash a success message if the note is valid
            new_note = Note(note=note, user_id=current_user.id)  # Create a new Note instance with the note content and the current user's ID
            db.session.add(new_note)  # Add the new note to the database session
            db.session.commit()  # Commit the session to save the new note to the database
    return render_template('home.html', title='Home', user=current_user)  # Render the home page template with the current user


@views.route('/delete-note', methods=["POST"])  # Route to delete a note
@login_required  # This decorator ensures that only logged-in users can access this route
def delete_note():
    note=json.loads(request.data)  # Load the JSON data from the request
    note_id = note['noteId']  # Extract the note ID from the JSON data
    note = Note.query.get(note_id) #return the whole note object with the given ID
    #means whole table with that id
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash ("Note deleted successfully", category='success')
    else:
        flash ("Note not found", category='error')
    return jsonify({})  # Return an empty JSON response
@views.route('/customer', methods=["GET", "POST"])  # Route for customer information
@login_required  # This decorator ensures that only logged-in users can access this route
def customer():
    if request.method == "POST":
        if request.form.get('show-customers')=="":
            return redirect(url_for('views.all'))
        
        mobile = request.form.get('mobile')
        name = request.form.get('name')
        if len(mobile) < 10:
            flash("Mobile number must be at least 10 digits.", category='error')
        elif len(name) < 1:
            flash("Too short name", category='error')
        else:
            new_customer = Customer(mobile=mobile, name=name, user_id=current_user.id)
            db.session.add(new_customer)
            db.session.commit()  # Commit the session to save the new customer to the database
            flash("Customer information submitted successfully!", category='success')
            return redirect(url_for('views.customer'))
    return render_template('customer.html', title='Customer', user=current_user)  # Render the customer page template with the current user
# This route is for displaying and processing customer information

@views.route('/all', methods=["GET"])  # Route to display all customers
@login_required  # This decorator ensures that only logged-in users can access this route
def all():
    return render_template('all.html', title='All Customers', user=current_user)
