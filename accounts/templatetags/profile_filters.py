from datetime import date, datetime

from django import template


register = template.Library()


@register.filter
def calculate_age(born):
    today = date.today()
    birth_date = datetime.strptime(str(born), "%Y-%m-%d").date()
    age = today.year - birth_date.year
    return age
