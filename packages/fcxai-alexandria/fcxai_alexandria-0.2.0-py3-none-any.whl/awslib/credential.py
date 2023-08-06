import boto3


def get_aws_client(service_name, region_name, **kwargs):
    session = get_aws_session(**kwargs)
    client = session.client(service_name=service_name, region_name=region_name)
    return client


def get_aws_session(aws_access_key=None, aws_secret_key=None):
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )
    return session
