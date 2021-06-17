from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from . import db

class User(db.Model):
     __tablename__ = "users"

     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(64), index=False, unique=True, nullable=False)
     password = db.Column(db.String(100), nullable=False)
     balance = db.Column(db.Float, server_default="0", nullable=True)
     created = db.Column(db.DateTime, server_default=db.func.now())
     updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

     def __init__(self, username, password, balance=0):
         self.username = username
         self.password = generate_password_hash(password, method='sha256')
         self.balance = balance

     def add(self):
         db.session.add(self)
         db.session.commit()

     @staticmethod
     def access_token(username):
         return create_access_token(identity=username)

     @staticmethod
     def refresh_token(username):
         return create_refresh_token(identity=username)

     def verify_password(self, password):
         return check_password_hash(self.password, password)

     def info(self):
         return {
             "id":self.id,
             "username":self.username,
             "email":self.email,
             "balance":self.balance
         }

     def __repr__(self):
         return f"<User {self.id}"

class Category(db.Model):
     __tablename__ = 'categories'

     id = db.Column(db.Integer,primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
     name = db.Column(db.Text, nullable=False)
     activity = db.Column(db.Float, server_default="0", nullable=True)
     balance = db.Column(db.Float, server_default="0", nullable=True)
     created = db.Column(db.DateTime, server_default=db.func.now())
     updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

     user = db.relationship('User', backref=db.backref('users', lazy=True))

     def __init__(self, user_id, name, activity=0, balance=0):
         self.user_id = user_id
         self.name = name
         self.activity = activity
         self.balance = balance

     def add(self):
         db.session.add(self)
         db.session.commit()

     def update(self, name, activity, balance):
         self.name = name
         self.activity = activity
         self.balance = balance
         
         db.session.commit()

         return self

     def delete(self):
         db.session.delete(self)
         db.session.commit()

         return self

     def __repr__(self):
         return f"<Category {self.id}>"

class Item(db.Model):
     __tablename__ = 'items'

     id = db.Column(db.Integer, primary_key=True)
     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
     name = db.Column(db.Text, nullable=False)
     activity = db.Column(db.Float, server_default="0", nullable=True)
     balance = db.Column(db.Float, server_default="0", nullable=True)
     created = db.Column(db.DateTime, server_default=db.func.now())
     updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
     
     category = db.relationship('Category', backref=db.backref('categories', lazy=True))

     def __init__(self, category_id, name, activity=0, balance=0):
         self.category_id = category_id
         self.name = name
         self.activity = activity
         self.balance = balance

     def add(self):
         db.session.add(self)
         db.session.commit()
    
     def update(self,name, activity, balance):
         self.name = name
         self.activity = activity
         self.balance = balance
         
         db.session.commit()

         return self

     def delete(self):
         db.session.delete(self)
         db.session.commit()

         return self

     def __repr__(self):
         return f"<Item {self.id}>"

class RevokedToken(db.Model):
     __tablename__ = "revoked_tokens"

     id = db.Column(db.Integer, primary_key=True)
     jti = db.Column(db.String(120))

     def __init__(self, jti):
         self.jti = jti
     
     def add(self):
         db.session.add(self)
         db.session.commit()

     @classmethod
     def is_jti_blacklisted(cls, jti):
         query = cls.query.filter_by(jti=jti).first()
         return bool(query)