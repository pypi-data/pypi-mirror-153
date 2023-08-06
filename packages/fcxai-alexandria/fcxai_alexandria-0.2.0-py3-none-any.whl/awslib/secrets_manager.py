# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/
import base64
import json

import boto3
from awslib import get_aws_client
from botocore.exceptions import ClientError


def get_secret(secret_key, secret_name, region_name, **kwargs):
    """
    Get secrets from aws 'secret manager'

    :param secret_key: Secret manager key to be retrieved
    :param secret_name: Secret name
    :param region_name: AWS region
    :param kwargs: AWS acess keys used to get session, if empyt session will search keys in another places
    :return Depending on whether the secret is a string or binary, one of these fields will be populated.
    """

    client = get_aws_client("secretsmanager", region_name, **kwargs)

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        secret = (
            get_secret_value_response["SecretString"]
            if "SecretString" in get_secret_value_response
            else base64.b64decode(get_secret_value_response["SecretBinary"])
        )
        secret_dict = json.loads(secret)
        return secret_dict[secret_key]
