import unittest
import ujson

from app import create_app, db
from app.models import User, Category

class BudgetTressaTestCase(unittest.TestCase):
     def setUp(self):
         self.app = create_app(config_name='testing')
         self.client = self.app.test_client
         self.url_prefix = "/api/v1"
         self.access_token = None
         self.refresh_token = None
         self.user =  {
             "username":"test_username",
             "password":"test_password"
         }
         self.invalid_username = {
             "username":"test_username1",
             "password":"test_password"  
         }
         self.invalid_password = {
             "username":"test_username",
             "password":"test_password1"  
         }
         self.category = {
             "name":"Daily Expenses",
             "balance":200
         }
         self.category_update = {
             "name":"Daily Expenses",
             "activity":"100",
             "balance":100
         }
         self.item = {
             "name":"Dinner",
             "balance":100
         }
         self.item_update = {
             "name":"Dinner",
             "activity":"50",
             "balance":50
         }

         with self.app.app_context():
             db.create_all()

     def get_login_tokens(self):
         # Signup  
         res = self.client().post(f"{self.url_prefix}/signup", json=self.user)
         # Login 
         res = self.client().post(f"{self.url_prefix}/login", json=self.user)
      
         data = ujson.loads(res.data)

         return data['data']['access_token'], data['data']['refresh_token']

     def headers(self, token):
         return {'Authorization':f"Bearer {token}"}

     def test_health_check(self):
         res = self.client().get(f"{self.url_prefix}/health-check")
         self.assertEqual(res.status_code, 200)
     
     # Auth 
     def test_auth(self):
         # Signup  
         res = self.client().post(f"{self.url_prefix}/signup", json=self.user)
         self.assertEqual(res.status_code, 201)
         self.assertIn(f"{self.user['username']} is created.", str(res.data))

         # Duplicate User
         res = self.client().post(f"{self.url_prefix}/signup", json=self.user)
         self.assertEqual(res.status_code, 409)
         self.assertIn(f"Username already taken", str(res.data)) 

         # Login 
         res = self.client().post(f"{self.url_prefix}/login", json=self.user)
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"Logged in as {self.user['username']}.", str(res.data))        

         data = ujson.loads(res.data)

         if self.access_token == None:
             self.access_token = data['data']['access_token']

         if self.refresh_token == None:
             self.refresh_token = data['data']['refresh_token']

         # Invalid Username 
         res = self.client().post(f"{self.url_prefix}/login", json=self.invalid_username)
         self.assertEqual(res.status_code, 401)
         self.assertIn(f"User doesn\\\'t exist.", str(res.data))       

         # Invalid Password 
         res = self.client().post(f"{self.url_prefix}/login", json=self.invalid_password)
         self.assertEqual(res.status_code, 401)
         self.assertIn(f"Password is wrong.", str(res.data))   

         # Refresh Token  
         res = self.client().post(
             f"{self.url_prefix}/refresh-token", 
             headers=self.headers(self.refresh_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"Token refreshed for", str(res.data))

         # Revoke Access Token  
         res = self.client().post(
             f"{self.url_prefix}/revoke-access-token", 
             headers=self.headers(self.access_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"Access token has been revoked.", str(res.data))  

         # Revoke Refresh Token    
         res = self.client().post(
             f"{self.url_prefix}/revoke-refresh-token", 
             headers=self.headers(self.refresh_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"Refresh token has been revoked.", str(res.data))
     
     # Category  
     def test_category(self):
         tokens = self.get_login_tokens()
         if self.access_token == None:
             self.access_token = tokens[0]

         if self.refresh_token == None:
             self.refresh_token = tokens[1]
         
         # Add Category  
         res = self.client().post(
             f"{self.url_prefix}/categories", 
             headers=self.headers(self.access_token), 
             json=self.category
         )
         self.assertEqual(res.status_code, 201)
         self.assertIn(f"success", str(res.data))

         # Get All Category 
         res = self.client().get(
             f"{self.url_prefix}/categories", 
             headers=self.headers(self.access_token), 
             json=self.category
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))

         # Get Category  
         res = self.client().get(
             f"{self.url_prefix}/categories/1",
             headers=self.headers(self.access_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))

         # Update Category 
         res = self.client().put(
             f"{self.url_prefix}/categories/1", 
             headers=self.headers(self.access_token), 
             json=self.category_update
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))
         
         # Delete Category 
         res = self.client().delete(
             f"{self.url_prefix}/categories/1", 
             headers=self.headers(self.access_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))

     def test_item(self):
         tokens = self.get_login_tokens()
         if self.access_token == None:
             self.access_token = tokens[0]

         if self.refresh_token == None:
             self.refresh_token = tokens[1]

         # Add Category  
         res = self.client().post(
             f"{self.url_prefix}/categories", 
             headers=self.headers(self.access_token), 
             json=self.category
         )
         self.assertEqual(res.status_code, 201)
         self.assertIn(f"success", str(res.data))

         # Get All Items
         res = self.client().get(
             f"{self.url_prefix}/categories/1/items",
              headers=self.headers(self.access_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))

         # Add Item  
         res = self.client().post(
             f"{self.url_prefix}/categories/1/items", 
             headers=self.headers(self.access_token), 
             json=self.item
         )
         self.assertEqual(res.status_code, 201)
         self.assertIn(f"success", str(res.data))

         # Get Item 
         res = self.client().get(
             f"{self.url_prefix}/categories/1/items/1",
             headers=self.headers(self.access_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))

         # Update Item  
         res = self.client().put(
             f"{self.url_prefix}/categories/1/items/1", 
             headers=self.headers(self.access_token), 
             json=self.item_update
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))

         # Delete Item  
         res = self.client().delete(
             f"{self.url_prefix}/categories/1/items/1", 
             headers=self.headers(self.access_token)
         )
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"success", str(res.data))

     def tearDown(self):
         with self.app.app_context():
             db.session.remove()
             db.drop_all()

if __name__ == "__main__":
     unittest.main()