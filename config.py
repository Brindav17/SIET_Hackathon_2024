import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'  # Change to a random secret key
    DEBUG = os.environ.get('DEBUG') or True  # Set to False in production

    # Database configuration
    DATABASE = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'  # Default to SQLite

    # Other configurations can be added here
    # Example: 
    # SQLALCHEMY_DATABASE_URI = DATABASE
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
