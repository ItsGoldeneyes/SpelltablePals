'''
Testing framework for the backend.
Ensure that the backend app is running locally on port 5000 before running tests.
'''

import unittest
import requests
import json

class TestUserProfiles(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000/user_profiles'
        
    def test_post(self):