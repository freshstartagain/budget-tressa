from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from instance.config import app_config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_name):
     app = Flask(__name__, instance_relative_config=False)
     app.config.from_object(app_config[config_name])

     db.init_app(app)
     ma.init_app(app)
     jwt.init_app(app)
     Migrate(app, db)
    
     with app.app_context():
         from . api import api as api_blueprint
         app.register_blueprint(api_blueprint, url_prefix='/api/v1')

         from . models import RevokedToken
         @jwt.token_in_blocklist_loader
         def check_if_token_is_revoked(jwt_header, jwt_payload):
             jti = jwt_payload['jti']
             token =  RevokedToken.is_jti_blacklisted(jti)     

         return app



