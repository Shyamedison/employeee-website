import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Change this to a random secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///employees.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
