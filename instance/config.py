import os
from datetime import timedelta

class Config:
     DEBUG = False
     CSRF_ENABLE = True
     SECRET_KEY = os.environ['SECRET_KEY']

     SQLALCHEMY_ECHO = False
     SQLALCHEMY_TRACK_MODIFICATIONS = False   
     
     JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
     JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
     DEBUG = True
     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_DB_DEV_URI']

class TestingConfig(Config):
     TESTING = True
     DEBUG = True
     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_DB_TEST_URI']

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

