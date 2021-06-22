from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from .. models import User, Category
from .. schema import CategorySchema
from .. services.response_handler import success, error
from . import api

@api.route('/categories', methods=['GET','POST'])
@jwt_required()
def category():
     try:
         user = User.query.filter_by(username=get_jwt_identity()).first()
         
         if request.method == 'POST':
             content = request.get_json()
             name = content['name']
             balance = content['balance']

             category = Category.query.filter_by(name=name, user_id=user.id).first()

             if category:
                 return error(data={"error":"Category already existing."}, status_code=409)
            
             category_schema = CategorySchema()
             category = Category(user.id, name, balance)
             category.add()

             return success(data=category_schema.dump(category) , status_code=201)

         if request.method == 'GET':
             category_schema = CategorySchema(many=True)
             categories = Category.query.filter(Category.user_id == user.id).all()
             
             return success(data=category_schema.dump(categories))

     except Exception as e:
         return error(data={"error":e})

@api.route('/categories/<int:category_id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def get_update_delete_category(category_id):
     category_error_message = {"error":"Category is not existing."}

     try:
         user = User.query.filter_by(username=get_jwt_identity()).first()
         category_schema = CategorySchema()

         if request.method == 'GET':
             category = Category.query.filter_by(id=category_id, user_id=user.id).first()

             if not category:
                 return error(data=category_error_message, status_code=404)

             return success(data=category_schema.dump(category))

         if request.method == 'PUT':
             content = request.get_json()
             name = content['name']
             activity = content['activity']
             balance = content['balance']
             
             category = Category.query.filter_by(id=category_id, user_id=user.id).first()

             if not category:
                 return error(data=category_error_message, status_code=404)

             category.update(name, activity, balance)

             return success(data=category_schema.dump(category))

         if request.method == 'DELETE':
             category = Category.query.filter_by(id=category_id, user_id=user.id).first()

             if not category:
                 return error(data=category_error_message, status_code=404)

             category.delete()
             return success(data=category_schema.dump(category))

     except Exception as e:
         return error(data={"error":e})
