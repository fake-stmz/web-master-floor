from django import template

register = template.Library()

@register.filter
def phone_format(phone):
    return f'+7 {phone[:3]} {phone[3:6]} {phone[6:8]} {phone[8:]}'