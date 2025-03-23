import unittest
import json
from unittest.mock import patch, MagicMock
import time

from src.authorizer_function import lambda_handler, validate_token, generate_policy


class TestAuthorizerFunction(unittest.TestCase):
    
    @patch('src.authorizer_function.validate_token')
    def test_authorizer_function_valid_token(self, mock_validate_token):
        # Mock the token validation to return valid
        mock_validate_token.return_value = (True, {
            'sub': '123',
            'name': 'Test User',
            'cpf': '12345678900',
            'iat': int(time.time()),
            'exp': int(time.time()) + 3600
        })
        
        # Create a mock event
        event = {
            'authorizationToken': 'Bearer valid_token',
            'methodArn': 'arn:aws:execute-api:us-east-1:123456789012:abcdef123/dev/GET/auth'
        }
        
        # Call the lambda handler
        response = lambda_handler(event, {})
        
        # Check the response
        self.assertEqual(response['principalId'], '123')
        self.assertEqual(response['policyDocument']['Statement'][0]['Effect'], 'Allow')
    
    @patch('src.authorizer_function.validate_token')
    def test_authorizer_function_invalid_token(self, mock_validate_token):
        # Mock the token validation to return invalid
        mock_validate_token.return_value = (False, {})
        
        # Create a mock event
        event = {
            'authorizationToken': 'Bearer invalid_token',
            'methodArn': 'arn:aws:execute-api:us-east-1:123456789012:abcdef123/dev/GET/auth'
        }
        
        # Call the lambda handler
        response = lambda_handler(event, {})
        
        # Check the response
        self.assertEqual(response['principalId'], 'user')
        self.assertEqual(response['policyDocument']['Statement'][0]['Effect'], 'Deny')
    
    def test_authorizer_function_missing_token(self):
        # Create a mock event with missing token
        event = {
            'authorizationToken': 'No bearer token',
            'methodArn': 'arn:aws:execute-api:us-east-1:123456789012:abcdef123/dev/GET/auth'
        }
        
        # Call the lambda handler
        response = lambda_handler(event, {})
        
        # Check the response
        self.assertEqual(response['principalId'], 'user')
        self.assertEqual(response['policyDocument']['Statement'][0]['Effect'], 'Deny')
    
    def test_validate_token_valid(self):
        # Create and validate a valid token (would need a real token to test)
        # This is a simplified test that would need to be expanded with a real token
        with patch('src.authorizer_function.time') as mock_time:
            mock_time.time.return_value = 1000
            
            # Since we can't easily create a real token, we'll mock internal functions
            with patch('src.authorizer_function.hmac.new') as mock_hmac:
                mock_digest = MagicMock()
                mock_hmac.return_value.digest.return_value = mock_digest
                
                with patch('src.authorizer_function.base64.urlsafe_b64decode') as mock_b64decode:
                    mock_b64decode.return_value = json.dumps({
                        'sub': '123',
                        'exp': 2000  # Later than our mocked time
                    }).encode()
                    
                    with patch('src.authorizer_function.base64.urlsafe_b64encode') as mock_b64encode:
                        mock_b64encode.return_value.decode.return_value.rstrip.return_value = "signature"
                        
                        # Test with a mock token with 3 parts
                        is_valid, claims = validate_token("header.payload.signature")
                        
                        # Validate token should succeed
                        self.assertTrue(is_valid)
                        self.assertEqual(claims['sub'], '123')
    
    def test_generate_policy(self):
        # Test policy generation
        policy = generate_policy('123', 'Allow', 'arn:aws:execute-api:region:account:api/stage/method/resource')
        
        # Check the policy
        self.assertEqual(policy['principalId'], '123')
        self.assertEqual(policy['policyDocument']['Version'], '2012-10-17')
        self.assertEqual(policy['policyDocument']['Statement'][0]['Effect'], 'Allow')
        
        # Test with context
        policy_with_context = generate_policy(
            '123', 
            'Allow', 
            'arn:aws:execute-api:region:account:api/stage/method/resource',
            {'key': 'value'}
        )
        
        # Check the policy
        self.assertEqual(policy_with_context['context']['key'], 'value')


if __name__ == '__main__':
    unittest.main() 