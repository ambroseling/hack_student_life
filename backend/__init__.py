import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Create the extensions first
load_dotenv(dotenv_path='.env.dev', override=True)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://hacksl:hacksl@localhost:5432/hacksl_db"
    
    # Initialize extensions with app
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
    return app

# Create an app instance
app = create_app()