from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from .. models import User, RevokedToken
from .. services.response_handler import success, error
from . import api

@api.route('/signup', methods=['POST'])
def signup():
     content = request.get_json()

     username = content['username']
     password = content['password']

     user = User.query.filter_by(username=username).first()
    
     if user:
         return error(data={"error":"Username already taken."}, status_code=409)

     try:            
         new_user = User(username, password)
         new_user.add()
        
         data = {
             "message":f"{new_user.username} is created.",
             "access_token":f"{User.access_token(new_user.username)}",
             "refresh_token":f"{User.refresh_token(new_user.username)}"
         }

         return success(data=data, status_code=201)

     except Exception as e:
         return error(data={"error":e})

@api.route('/login', methods=['POST'])
def login():
     try:   
         content = request.get_json()
         username = content['username']
         password = content['password']

         user = User.query.filter_by(username=username).first()

         if not user:
             return error(data={"error":"User doesn't exist."}, status_code=401)
        
         if not user.verify_password(password):
             return error(data={"error":"Password is wrong."}, status_code=401)
        
         data = {
             "message":f"Logged in as {user.username}.",
             "access_token":f"{User.access_token(user.username)}",
             "refresh_token":f"{User.refresh_token(user.username)}"
         }

         return success(data=data)

     except Exception as e:
         return error(data={"error":e})

@api.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
     try:   
         current_user = get_jwt_identity()

         data = {
             "message":f"Token refreshed for {current_user}.",
             "access_token":User.access_token(current_user),
             "refresh_token":User.refresh_token(current_user)
         }

         return success(data=data)
         
     except Exception as e:
         return error(data={"error":e}) 

@api.route('/revoke-access-token', methods=['POST'])
@jwt_required()
def revoke_access():
     try:   
         jti = get_jwt()['jti']
         revoked_token = RevokedToken(jti)
         revoked_token.add()

         data = {"message":"Access token has been revoked."}

         return success(data=data)
         
     except Exception as e:
         return error(data={"error":e}) 

@api.route('/revoke-refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def revoke_refresh():
     try:   
         jti = get_jwt()['jti']
         revoked_token = RevokedToken(jti)
         revoked_token.add()

         data = {"message":"Refresh token has been revoked."}

         return success(data=data)
         
     except Exception as e:
         return error(data={"error":e}) 