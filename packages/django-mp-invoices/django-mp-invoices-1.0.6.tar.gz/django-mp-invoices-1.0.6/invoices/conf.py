
from django.conf import settings


invoice_settings = getattr(settings, 'INVOICES', {})

IS_ROUNDING_ENABLED = invoice_settings.get('IS_ROUNDING_ENABLED', True)

IS_PRODUCT_PRICE_SHOWN_IN_DEFAULT_CURRENCY = invoice_settings.get(
    'IS_PRODUCT_PRICE_SHOWN_IN_DEFAULT_CURRENCY', True)

IS_PRODUCT_SELECT_COLLAPSED = invoice_settings.get(
    'IS_PRODUCT_SELECT_COLLAPSED', True)
