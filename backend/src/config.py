import os

load_dotenv()

class Config:
    # MariaDB connection string
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/flight_game'
    
    # Works faster with enabled this one
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')

    # for debugging
    SQLALCHEMY_ECHO = True

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/flight_game'