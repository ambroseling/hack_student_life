import os 
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Create the extensions first
load_dotenv(dotenv_path='.env.dev', override=True)

db = SQLAlchemy()

def create_app():
    api = Blueprint('api', __name__)
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.register_blueprint(api, url_prefix='/api')
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
    return app

# Create an app instance
application = create_app()