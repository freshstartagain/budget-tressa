from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from .. models import User, Category, Item
from .. schema import ItemSchema
from .. services.response_handler import success, error
from . import api

@api.route('/categories/<int:category_id>/items', methods=['GET','POST'])
@jwt_required()
def item(category_id):
     def validate_category(category_id):
         category = Category.query.filter_by(id=category_id, user_id=user.id).first()

         if not category:
             return error(data={"error":"Category is not existing."}, status_code=404)

         return category

     try:
         user = User.query.filter_by(username=get_jwt_identity()).first()

         if request.method == 'POST':
             content = request.get_json()
             name = content['name']
             balance = content['balance']
             
             category = validate_category(category_id)

             item = Item.query.filter_by(name=name, category_id=category.id).first()

             if item:
                 return error(data={"error":"Item already existing."}, status_code=409)
             
             item_schema = ItemSchema()
             item = Item(category.id, name, balance)
             item.add()

             data = item_schema.dump(item)

             return success(data=data, status_code=201)

         if request.method == 'GET':
             category = validate_category(category_id)

             item_schema = ItemSchema(many=True)
             items = Item.query.filter_by(category_id=category.id).all()
             
             data = item_schema.dump(items)
             
             return success(data=data)

     except Exception as e:
         return error(data={"error":e})

@api.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def get_update_delete_item(category_id, item_id):
     def validate_category_item(category_id, item_id):
         category = Category.query.filter_by(id=category_id, user_id=user.id).first()

         if not category:
             return error(data=category_error_message, status_code=404)

         item = Item.query.filter_by(category_id=category.id, id=item_id).first()

         if not item:
             return error(data=item_error_message, status_code=404)

         return item

     try:
         user = User.query.filter_by(username=get_jwt_identity()).first()
         item_schema = ItemSchema()
         category_error_message = {"error":"Category is not existing."}
         item_error_message = {"error":"Item is not existing."}
         
         if request.method == 'GET':
             item = validate_category_item(category_id, item_id)

             data = item_schema.dump(item)

             return success(data=data)
             
         if request.method == 'PUT':
             content = request.get_json()
             name = content['name']
             activity = content['activity']
             balance = content['balance']

             item = validate_category_item(category_id, item_id)

             item.update(name, activity, balance)

             data = item_schema.dump(item)

             return success(data=data)

         if request.method == 'DELETE':
             item = validate_category_item(category_id, item_id)
             
             item.delete()

             data = item_schema.dump(item)

             return success(data=data)

     except Exception as e:
         return error(data={"error":e})