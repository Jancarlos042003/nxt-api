import logging

from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table

from app.exceptions.technical_exceptions import DatabaseException

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, table: Table):
        self.table = table

    def get_user(self, username: str):
        try:
            response = self.table.get_item(Key={"username": username})
        except ClientError as err:
            logger.error(
                "No se pudo obtener al usuario con username %s desde la tabla %s. %s: %s",
                username,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise DatabaseException(err)
        else:
            return response.get("Item")
