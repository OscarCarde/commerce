from django import template
import decimal

register = template.Library()

@register.filter
def round_decimal(value: object) -> str:
    if value == None:
        return ""
        
    return str(round(decimal.Decimal(value), 2))
