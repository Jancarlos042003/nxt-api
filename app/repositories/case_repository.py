import logging

from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table

from app.exceptions.technical_exceptions import DatabaseException

logger = logging.getLogger(__name__)


class CaseRepository:
    def __init__(self, table: Table):
        self.table = table

    def create_case(self, case: dict):
        try:
            self.table.put_item(Item=case)
        except ClientError as err:
            logger.error(
                "No se pudo agregar el caso %s a la tabla %s. %s: %s",
                case.get("name", "Desconocido"),
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise DatabaseException(str(err))

    def get_case(self, case_id: str):
        try:
            response = self.table.get_item(Key={"id": case_id})
        except ClientError as err:
            logger.error(
                "No se pudo obtener el caso con ID %s desde la tabla %s. %s: %s",
                case_id,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise DatabaseException(str(err))
        else:
            return response.get("Item")

    def list_cases(self):
        cases = []
        scan_kwargs = {}

        try:
            done = False
            start_key = None

            while not done:
                if start_key:
                    scan_kwargs["ExclusiveStartKey"] = start_key

                response = self.table.scan(**scan_kwargs)
                cases.extend(response.get("Items", []))

                start_key = response.get("LastEvaluatedKey")
                done = start_key is None
        except ClientError as err:
            logger.error(
                "Error al escanear todos los casos. %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise DatabaseException(str(err))

        return cases

    def update_case(self, case_id: str, update_data: dict):
        """
        Actualiza solo los campos proporcionados en update_data.
        update_data: diccionario con los campos a actualizar
        """
        if not update_data:
            # No hay nada que actualizar
            return self.get_case(case_id)

        # Construir expresión de actualización dinámica
        update_parts = []
        expression_values = {}
        expression_names = {}

        for key, value in update_data.items():
            placeholder = f":{key[0]}"
            attr_name = f"#{key}"

            update_parts.append(f"{attr_name} = {placeholder}")
            expression_values[placeholder] = value
            expression_names[attr_name] = key

        update_expression = "SET " + ", ".join(update_parts)

        # if case.name is not None:
        #     update_parts.append("name = :n")
        #     expression_values[":n"] = case.name
        #
        # if case.description is not None:
        #     update_parts.append("description = :d")
        #     expression_values[":d"] = case.description
        #
        # if case.status is not None:
        #     update_parts.append("#st = :s")
        #     expression_values[":s"] = case.status
        #
        # update_expression = "SET " + ", ".join(update_parts)

        try:
            response = self.table.update_item(
                Key={"id": case_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="ALL_NEW",
            )
        except ClientError as err:
            logger.error(
                "No se pudo actualizar el caso con ID %s en la tabla %s. %s: %s",
                case_id,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise DatabaseException(str(err))
        else:
            return response.get("Attributes")

    def delete_case(self, case_id: str):
        try:
            self.table.delete_item(Key={"id": case_id})
        except ClientError as err:
            logger.error(
                "No se pudo eliminar el caso con ID %s. %s: %s",
                case_id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise DatabaseException(str(err))
