"""
Test cases for the API simulation using unittest.
"""

import unittest
import requests

class TestAPISimulation(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/fitness-data"

    def test_api_response_status(self):
        """Test that the API responds with a 200 status code."""
        response = requests.get(self.API_URL)
        self.assertEqual(response.status_code, 200)

    def test_api_response_structure(self):
        """Test that the API response contains the required keys."""
        response = requests.get(self.API_URL)
        data = response.json()
        self.assertIn("user_id", data)
        self.assertIn("timestamp", data)
        self.assertIn("steps", data)
        self.assertIn("heart_rate", data)

    def test_invalid_user_id(self):
        """Test that the API handles invalid user IDs."""
        response = requests.get(f"{self.API_URL}?user_id=11")
        self.assertEqual(response.status_code, 400)
        error_data = response.json()
        self.assertIn("error", error_data)

if __name__ == '__main__':
    unittest.main()
