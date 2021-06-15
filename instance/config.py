from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
     DEBUG = False
     CSRF_ENABLE = True
     SECRET_KEY = environ.get('SECRET_KEY')

     SQLALCHEMY_ECHO = False
     SQLALCHEMY_TRACK_MODIFICATIONS = False   
     
     JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
     JWT_ACCESS_TOKEN_EXPIRES = environ.get('JWT_ACCESS_TOKEN_EXPIJWT_SECRET_KEY')

class DevelopmentConfig(Config):
     DEBUG = True
     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, environ.get('SQLALCHEMY_DATABASE_URI'))  

class TestingConfig(Config):
     TESTING = True
     DEBUG = True
     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, environ.get('SQLALCHEMY_DATABASE_URI'))  

class StagingConfig(Config):
     DEBUG = True

class ProductionConfig(Config):
     DEBUG = False
     TESTING = False

app_config = {
     'development': DevelopmentConfig,
     'testing': TestingConfig,
     'staging': StagingConfig,
     'production':ProductionConfig
}