import json

import boto3
from botocore.exceptions import ClientError


def get_aws_secret(secret_name: str, region_name: str) -> str:
    """
    Fetches the API key from AWS Secrets Manager.
    Args:
        secret_name (str): The name of the secret in AWS Secrets Manager.
        region_name (str): The AWS region where the secret is stored.
    Returns:
        str: The API key stored in the secret.
    Raises:
        Exception: If the secret cannot be retrieved or parsed.
    """
    # Create a Secrets Manager client.
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise Exception(f"Unable to retrieve secret: {e}")

    secret = get_secret_value_response.get("SecretString")
    if not secret:
        raise Exception("SecretString is empty or not found in the response.")

    # If the secret is a key-value string, parse and return the JSON.
    try:
        return json.loads(secret)
    except json.JSONDecodeError:
        # If the secret is plain text, return it as is.
        return secret
