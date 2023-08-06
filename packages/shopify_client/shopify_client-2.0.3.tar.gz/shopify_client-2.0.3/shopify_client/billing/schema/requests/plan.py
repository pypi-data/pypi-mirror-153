import dataclasses

from shopify_client.billing.schema.requests.recurring_pricing_details import RecurringPricingDetails


@dataclasses.dataclass
class Plan:
    appRecurringPricingDetails: RecurringPricingDetails
