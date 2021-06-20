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
     JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
     DEBUG = True
     SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{environ.get('DATABASE_USER')}:{environ.get('DATABASE_PASSWORD')}@db:{environ.get('DATABASE_HOST')}/{environ.get('DATABASE_DB_DEV')}"

class TestingConfig(Config):
     TESTING = True
     DEBUG = True
     SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{environ.get('DATABASE_USER')}:{environ.get('DATABASE_PASSWORD')}@db:{environ.get('DATABASE_HOST')}/{environ.get('DATABASE_DB_TEST')}"

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

