import unittest
import os
import json
from app import create_app, db

class BudgetTressaTestCase(unittest.TestCase):
     def setUp(self):
         self.app = create_app(config_name='testing')
         self.client = self.app.test_client

         with self.app.app_context():
             db.create_all()
     
     def test_health_check(self):
         res = self.client().get('/api/v1/health-check')
         self.assertEqual(res.status_code, 200)

     def test_signup(self):
         data = {
             'username':'test_1',
             'password':'test_password'
         }
         res = self.client().post('/api/v1/signup', data=data)
         self.assertEqual(res.status_code, 200)
     
     def tearDown(self):
         with self.app.app_context():
             db.session.remove()
             db.drop_all()

if __name__ == "__main__":
     unittest.main()