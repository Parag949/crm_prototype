#this makes the website folder a python package


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 
from flask_login import LoginManager
db = SQLAlchemy()  # Initialize the database object
DB_NAME = "crm.db"  # Database name
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"]="your_secret_key_here" #encrypts cookies and session data

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Database URI  #create a SQLite database with the name crm.db and locate it in the same directory as the app
    db.init_app(app)  # Initialize the database with the Flask app
    

    from .views import views #import views blueprint
    from .auth import auth #import auth blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')    
    from .models import User, Note, Customer  #we are importing models here to ensure they are registered with SQLAlchemy so that models.py files run before we create the database
    #so all the classes in models.py will be registered with SQLAlchemy, here user and note

    create_database(app)

    login_manager = LoginManager()  # Initialize the login manager
    login_manager.login_view = 'auth.login'  # Set the login view to the auth blueprint's login route
    login_manager.init_app(app)  # Initialize the login manager with the Flask app
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Load a user by their primary key and check  it with whatever thing is passed hereit  is ID from the database

    return app


def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
    else:
        print('Database already exists.')  # Print a message indicating the database already exists
