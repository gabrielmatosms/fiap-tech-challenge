import json
import os
import time
import hmac
import hashlib
import base64
from typing import Dict, Any

# Environment variables
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda authorizer function for API Gateway.
    This function validates JWT tokens and authorizes requests.
    
    Args:
        event: The event dict containing the request parameters
        context: The context object provided by AWS Lambda
        
    Returns:
        An IAM policy document to authorize or deny the request
    """
    try:
        # Extract token from the Authorization header
        auth_header = event.get('authorizationToken', '')
        if not auth_header.startswith('Bearer '):
            return generate_policy('user', 'Deny', event['methodArn'])
        
        token = auth_header.replace('Bearer ', '')
        
        # Validate token
        is_valid, claims = validate_token(token)
        
        if is_valid:
            # If token is valid, generate an Allow policy
            return generate_policy(claims.get('sub', 'user'), 'Allow', event['methodArn'], claims)
        else:
            # If token is invalid, generate a Deny policy
            return generate_policy('user', 'Deny', event['methodArn'])
            
    except Exception as e:
        # In case of any errors, deny access
        print(f"Error: {str(e)}")
        return generate_policy('user', 'Deny', event['methodArn'])

def validate_token(token: str) -> tuple:
    """
    Validate a JWT token.
    
    Args:
        token: The JWT token to validate
        
    Returns:
        A tuple of (is_valid, claims)
    """
    # In a real implementation, you would use a proper JWT library
    # For example: import jwt
    try:
        # Split token into parts
        parts = token.split('.')
        if len(parts) != 3:
            return False, {}
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Decode payload to get claims
        payload_json = base64.urlsafe_b64decode(payload_b64 + '=' * (4 - len(payload_b64) % 4))
        claims = json.loads(payload_json)
        
        # Check token expiration
        if 'exp' in claims and claims['exp'] < time.time():
            return False, {}
            
        # Verify signature
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(
            SECRET_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip('=')
        
        if signature_b64 != expected_signature_b64:
            return False, {}
            
        return True, claims
        
    except Exception as e:
        print(f"Token validation error: {str(e)}")
        return False, {}

def generate_policy(principal_id: str, effect: str, resource: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate an IAM policy document.
    
    Args:
        principal_id: The principal ID (typically user ID)
        effect: 'Allow' or 'Deny'
        resource: The resource ARN
        context: Additional context data to pass to the backend
        
    Returns:
        An IAM policy document
    """
    auth_response = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        }
    }
    
    # Add context if provided
    if context:
        auth_response['context'] = context
    
    return auth_response 