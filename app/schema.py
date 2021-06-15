from . import ma

class UserSchema(ma.Schema):
     class Meta:
         fields = ("id","username", "email", "created", "updated")

class ItemSchema(ma.Schema):
     class Meta:
         fields = ("id","name", "balance", "created", "updated")

class CategorySchema(ma.Schema):
     class Meta:
         fields = ("id","name", "balance", "created", "updated")