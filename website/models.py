from . import db
from flask_login import UserMixin # Import UserMixin for user management
from sqlalchemy.sql import func

class Note(db.Model):  # Model for notes
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the note
    note = db.Column(db.String(1000))  # Content of the note
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp when the note was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#here "user" class will be is small as it is a syantax
      # Foreign key to link to the user who created the note
    # foreign key is always a column in the current table that references the primary key of another table

class User(db.Model, UserMixin): #only for user objects, not for other objects like contacts
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    email = db.Column(db.String(150), unique=True)  # Unique email for the user
    first_name = db.Column(db.String(150))  # First name of the user
    password = db.Column(db.String(150))  # Password for the user
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp when the user was created
    notes=db.relationship('Note')#here capital #this will tell flask alchmy, every time we  create a Note ,add into this user notes relationship that note id
    #so it will be a list which stores all diffent notes
    # Relationship to the Note model, allowing access to notes created by the user 