import boto3
from mypy_boto3_dynamodb.service_resource import Table

from app.core.config import settings


def get_dynamodb_resource():
    """Crear recurso de DynamoDB"""
    return boto3.resource('dynamodb', region_name=settings.AWS_REGION_NAME)


def get_dynamo_table() -> Table:
    """Dependencia para inyectar la tabla de casos"""
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(settings.CASES_TABLE)


def get_dynamo_table_users() -> Table:
    """Dependencia para inyectar la tabla de usuarios"""
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(settings.USERS_TABLE)
