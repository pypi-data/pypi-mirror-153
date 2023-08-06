from enum import Enum


class SupportedClient(Enum):
    BILLING = 'billing'
    WEBHOOK = 'webhook'
    SCRIPT_TAG = 'script_tag'
    STORE_PROPERTIES = 'store_properties'
    PRODUCT = 'product'
    BULK_OPERATIONS = 'bulk_operations'
