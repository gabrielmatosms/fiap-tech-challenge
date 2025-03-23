import json
import unittest
from unittest.mock import patch, MagicMock

from src.auth_function import lambda_handler, generate_token


class TestAuthFunction(unittest.TestCase):
    
    @patch('src.auth_function.requests.get')
    def test_auth_function_success(self, mock_get):
        # Mock the response from the customer API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "name": "Test User",
            "cpf": "12345678900",
            "email": "test@example.com"
        }
        mock_get.return_value = mock_response
        
        # Create a mock event
        event = {
            "body": json.dumps({"cpf": "12345678900"})
        }
        
        # Call the lambda handler
        response = lambda_handler(event, {})
        
        # Check the response
        self.assertEqual(response['statusCode'], 200)
        
        # Parse the response body
        body = json.loads(response['body'])
        self.assertEqual(body['message'], "Authentication successful")
        self.assertIn('token', body)
        self.assertIn('customer', body)
    
    @patch('src.auth_function.requests.get')
    def test_auth_function_invalid_cpf(self, mock_get):
        # Mock the response from the customer API for an invalid CPF
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Create a mock event
        event = {
            "body": json.dumps({"cpf": "00000000000"})
        }
        
        # Call the lambda handler
        response = lambda_handler(event, {})
        
        # Check the response
        self.assertEqual(response['statusCode'], 401)
        
        # Parse the response body
        body = json.loads(response['body'])
        self.assertEqual(body['message'], "Invalid CPF")
    
    def test_auth_function_missing_cpf(self):
        # Create a mock event with missing CPF
        event = {
            "body": json.dumps({})
        }
        
        # Call the lambda handler
        response = lambda_handler(event, {})
        
        # Check the response
        self.assertEqual(response['statusCode'], 400)
        
        # Parse the response body
        body = json.loads(response['body'])
        self.assertEqual(body['message'], "CPF is required")
    
    def test_generate_token(self):
        # Test token generation
        customer = {
            "id": 1,
            "name": "Test User",
            "cpf": "12345678900",
            "email": "test@example.com"
        }
        
        token = generate_token(customer)
        
        # Check that a token was generated (not empty)
        self.assertIsNotNone(token)
        self.assertTrue(len(token) > 0)
        
        # Check that the token has the correct format (three parts separated by dots)
        parts = token.split('.')
        self.assertEqual(len(parts), 3)


if __name__ == '__main__':
    unittest.main() 