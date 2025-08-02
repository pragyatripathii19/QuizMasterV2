from datetime import timedelta


# Base configuration class (can be extended for other environments)
class Config:
    DEBUG = False  # Disable debug mode by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable overhead of tracking object changes

# Configuration for local development (inherits from base Config)
class LocalDevelopmentConfig(Config):
    # Use SQLite as the development database
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"

    DEBUG = True  # Enable debug mode for development

    # Flask-Security settings
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Use bcrypt for hashing passwords
    SECURITY_PASSWORD_SALT = 'databrain1989secret'  # Salt for password hashing

    JWT_SECRET_KEY = "super-secret-jwt-key"   

    # General Flask settings
    SECRET_KEY = "databrain1989"  # Secret key for session management, CSRF, etc.
    WTF_CSRF_ENABLED = False  # Disable CSRF protection (useful for local dev or testing)

    

