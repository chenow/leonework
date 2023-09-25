from django.core.exceptions import ValidationError

from data_management.models import City, Profession


def check_city(value):
    cities = list(City.objects.values_list("city", flat=True))
    if value not in cities:
        raise ValidationError(f"{value} n'est pas une city acceptée.")
    return value


def check_poste(value):
    metiers = list(Profession.objects.values_list("profession", flat=True))
    if value not in metiers:
        raise ValidationError(f"{value} n'est pas un métier accepté.")
    return value
