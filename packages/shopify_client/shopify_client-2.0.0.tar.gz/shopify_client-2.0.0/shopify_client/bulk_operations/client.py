from .get import BulkOperationGet
from .orders import BulkOperationOrderClient


class BulkOperationsClient:
    @staticmethod
    def get(operation_input):
        return BulkOperationGet().execute(operation_input)

    @property
    def orders(self):
        return BulkOperationOrderClient
