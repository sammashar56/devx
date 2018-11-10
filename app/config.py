import os

class Config:
    """Sets the application running envirionnment"""
    SECRET_KEY = os.getenv('SECRET_KEY')
    PYENV = os.getenv("PYENV")

class Development(Config):
    """Variables for development env"""
    DEBUG=True
    TESTING=False

class Testing(Config):
    """Variables for testing env"""
    DEBUG=True
    TESTING=True

class Production(Config):
    """Variables for production env"""
    DEBUG=False
    TESTING=False

app_config = {
    "development":Development,
    "testing":Testing,
    "production":Production
}
