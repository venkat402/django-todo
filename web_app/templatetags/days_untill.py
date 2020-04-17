from datetime import datetime

from django import template

register = template.Library()


@register.filter
def days_until(date):
    diff = datetime.now().date() - datetime.date(date)

    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if (days > 1):
        return str(days) + " Days ago."
    else:
        return "Added recentlly."
