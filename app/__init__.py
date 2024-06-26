from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)



# Import and register routes after initializing extensions
from app.routes import user_routes

app.register_blueprint(user_routes.bp)

# Create database tables
with app.app_context():
    db.create_all()
