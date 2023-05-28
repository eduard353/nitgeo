from datetime import date

from django.core.exceptions import ValidationError


def validate_birth_date(value):
    if value.year < 1900:
        raise ValidationError('Invalid birth date - year must be greater then 1900.')
    age = (date.today() - value).days // 365
    if age < 18:
        raise ValidationError('Invalid birth date - your age must be at least 18 years old.')
