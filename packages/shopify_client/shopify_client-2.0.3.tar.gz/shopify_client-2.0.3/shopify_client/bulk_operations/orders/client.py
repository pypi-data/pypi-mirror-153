from .get import BulkOrdersGet


class BulkOperationOrderClient:
    @staticmethod
    def get():
        return BulkOrdersGet().execute()
