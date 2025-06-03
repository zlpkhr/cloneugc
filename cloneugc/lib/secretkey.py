from logging import getLogger

import boto3

logger = getLogger(__name__)

sm_client = boto3.client("secretsmanager")


def getsecretkey(name: str) -> str | None:
    try:
        response = sm_client.get_secret_value(SecretId=name)
        return response["SecretString"]
    except sm_client.exceptions.ResourceNotFoundException:
        logger.error(f"Secret key {name} does not exist")
        return None
