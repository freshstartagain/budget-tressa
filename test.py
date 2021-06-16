import unittest
import ujson

from app import create_app, db
from app.models import User

class BudgetTressaTestCase(unittest.TestCase):
     def setUp(self):
         self.app = create_app(config_name='testing')
         self.client = self.app.test_client
         self.url_prefix = "/api/v1"
         self.login_user = {
             "username":"test_username",
             "password":"test_password"
         }
         self.signup_user = {
             "username":"test_username_2",
             "password":"test-password"
         }
         
         with self.app.app_context():
             db.create_all()

             new_user = User(self.login_user['username'], self.login_user['password'])
             new_user.add()

             self.access_token = User.access_token(new_user.username)
             self.refresh_token = User.refresh_token(new_user.username)

     def test_health_check(self):
         res = self.client().get(f"{self.url_prefix}/health-check")
         self.assertEqual(res.status_code, 200)
     
     # Auth 
     def test_signup(self):
         res = self.client().post(f"{self.url_prefix}/signup", json=self.signup_user)
         self.assertEqual(res.status_code, 201)
         self.assertIn(f"{self.signup_user['username']} is created.", str(res.data))

     def test_login(self):
         res = self.client().post(f"{self.url_prefix}/login", json=self.login_user)
         self.assertEqual(res.status_code, 200) 
         self.assertIn(f"Logged in as {self.login_user['username']}", str(res.data))
    
     def test_refresh_token(self):
         res = self.client().post(f"{self.url_prefix}/refresh-token", headers={'Authorization':f"Bearer {self.refresh_token}"})
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"Token refreshed for", str(res.data))

     def test_revoke_access_token(self):
         res = self.client().post(f"{self.url_prefix}/revoke-access-token", headers={'Authorization':f"Bearer {self.access_token}"})
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"Access token has been revoked.", str(res.data))

     def test_revoke_refresh_token(self):
         res = self.client().post(f"{self.url_prefix}/revoke-refresh-token", headers={'Authorization':f"Bearer {self.refresh_token}"})
         self.assertEqual(res.status_code, 200)
         self.assertIn(f"Refresh token has been revoked.", str(res.data))

     # Category 

     def tearDown(self):
         with self.app.app_context():
             db.session.remove()
             db.drop_all()

if __name__ == "__main__":
     unittest.main()