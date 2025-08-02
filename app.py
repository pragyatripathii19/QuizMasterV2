# Import Flask class to create the app
from flask import Flask
from backend.models import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Import blueprints
from backend.auth_routes import auth_bp
from backend.quiz_routes import quiz_bp,questions_bp

# Import the config class from backend.config module
from backend.config import LocalDevelopmentConfig
import logging

# Factory function to create and configure the Flask app
def createApp():
    app = Flask(__name__)
    
    #CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:8080"]}}, supports_credentials=True)
    
    CORS(app, resources={r"/*": {
    "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
    "supports_credentials": True,
    "allow_headers": ["Content-Type", "Authorization"]
    }})


    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(quiz_bp, url_prefix="/quiz")
    app.register_blueprint(questions_bp)


    return app

# Create the app by calling the factory function
app = createApp()

# Define a route for the home page using the GET method
@app.get('/')
def home():
    return '<h1> home page</h1>'

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
