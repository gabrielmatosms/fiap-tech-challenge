# FIAP Lambda Auth

This repository contains the serverless authentication functions for the FIAP Tech Challenge project. It includes a Lambda function for CPF-based authentication and a Lambda authorizer for JWT token validation.

## Components

- **Auth Function**: Authenticates users based on their CPF by validating against the Customer API
- **Authorizer Function**: Validates JWT tokens for protected API endpoints

## Development

### Prerequisites

- Python 3.9+
- AWS SAM CLI
- AWS CLI (configured with appropriate credentials)

### Local Development

1. Clone the repository:
    ```bash
    git clone https://github.com/your-org/fiap-lambda-auth.git
    cd fiap-lambda-auth
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Run tests:
    ```bash
    pytest
    ```

4. Run linting:
    ```bash
    flake8 src tests
    ```

5. Build with SAM:
    ```bash
    sam build
    ```

6. Local testing:
    ```bash
    sam local invoke AuthFunction --event events/auth-event.json
    sam local invoke AuthorizerFunction --event events/authorizer-event.json
    ```

## Deployment

The repository is configured with GitHub Actions for CI/CD. The workflow will:

1. Run tests and lint code
2. Build the SAM application
3. Deploy to AWS (on push to main branch)

### Manual Deployment

You can also deploy manually:

```bash
sam build
sam deploy --guided
```

When prompted, provide the following parameters:
- Stack Name: `fiap-lambda-auth-stack`
- AWS Region: `your-aws-region`
- Parameter Environment: `dev` (or `qa`, `production`)
- Parameter SecretKey: `your-jwt-secret-key`
- Parameter CustomerApiUrl: `https://your-customer-api-url/customers`

## Environment Variables

The following environment variables are used by the Lambda functions:

- `CUSTOMER_API_URL`: URL for the Customer API (for AuthFunction)
- `SECRET_KEY`: Secret key for JWT token signing/validation (for AuthorizerFunction)

## Integration

The Lambda functions integrate with:

1. **Customer API**: To validate CPF and retrieve customer information
2. **API Gateway**: To provide authentication endpoints and JWT authorization

## License

[MIT License](LICENSE) 