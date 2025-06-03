import boto3

sm_client = boto3.client("secretsmanager")


def getsecretkey(name: str) -> str:
    response = sm_client.get_secret_value(SecretId=name)
    return response["SecretString"]
