import json
import os
import boto3
from typing import Dict, Any

# Environment variables
CUSTOMER_API_URL = os.environ.get("CUSTOMER_API_URL", "http://localhost:8000/customers")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function to authenticate users based on their CPF.
    This function will be integrated with API Gateway.
    
    Args:
        event: The event dict containing the request parameters
        context: The context object provided by AWS Lambda
        
    Returns:
        A response dict with authentication result
    """
    try:
        # Extract CPF from the request
        request_body = json.loads(event.get("body", "{}"))
        cpf = request_body.get("cpf")
        
        if not cpf:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "CPF is required"}),
                "headers": {"Content-Type": "application/json"},
            }
            
        # Call customer API to validate CPF
        # In a production environment, you would use boto3 to make HTTP requests
        # Here we'll use the requests library for simplicity in the example
        import requests
        
        response = requests.get(f"{CUSTOMER_API_URL}?cpf={cpf}")
        
        if response.status_code == 200:
            customer = response.json()
            
            # Generate a JWT token for the authenticated user
            # In a real implementation, you'd use a proper JWT library
            token = generate_token(customer)
            
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Authentication successful", "token": token, "customer": customer}),
                "headers": {"Content-Type": "application/json"},
            }
        elif response.status_code == 404:
            return {
                "statusCode": 401,
                "body": json.dumps({"message": "Invalid CPF"}),
                "headers": {"Content-Type": "application/json"},
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": "Error validating CPF"}),
                "headers": {"Content-Type": "application/json"},
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error: {str(e)}"}),
            "headers": {"Content-Type": "application/json"},
        }

def generate_token(customer: Dict[str, Any]) -> str:
    """
    Generate a JWT token for the authenticated user.
    
    Args:
        customer: The customer data
        
    Returns:
        A JWT token string
    """
    # In a real implementation, you'd use a proper JWT library
    # For example: import jwt
    # Here's a simplified example:
    
    import time
    import hmac
    import hashlib
    import base64
    
    # Create a header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # Create a payload with claims
    payload = {
        "sub": str(customer["id"]),
        "name": customer["name"],
        "cpf": customer["cpf"],
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,  # Token expires in 1 hour
    }
    
    # Convert to JSON and encode as base64
    header_json = json.dumps(header).encode()
    header_b64 = base64.urlsafe_b64encode(header_json).decode().rstrip('=')
    
    payload_json = json.dumps(payload).encode()
    payload_b64 = base64.urlsafe_b64encode(payload_json).decode().rstrip('=')
    
    # Create the signature
    # In production, use a proper secret key management system
    secret = "your-secret-key" 
    
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    # Combine to create JWT token
    token = f"{header_b64}.{payload_b64}.{signature_b64}"
    
    return token 