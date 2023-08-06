import shopify

from shopify_client.billing.charges.base_charge import BaseCharge


class OneTimePurchase(BaseCharge):
    @property
    def charge_type(self):
        return 'appPurchaseOneTime'

    @property
    def variable_type_string(self):
        return "$name: String!, $price: MoneyInput!, $returnUrl: URL!, $test: Boolean!"

    @property
    def variable_string(self):
        return "name: $name, price: $price, returnUrl: $returnUrl, test: $test"

    @property
    def charge_resource(self):
        return shopify.ApplicationCharge
