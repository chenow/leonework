import stripe
from companies.models import Company

from middleware import HttpRequestWithJob

from .models import Offer


def find_or_create_stripe_customer(request: HttpRequestWithJob):
    assert request.user.company is not None
    if not request.user.company.stripe_id:
        customer = stripe.Customer.create(
            description="Entreprise",
            email=request.user.email,
            name=request.user.company.name,
            phone=request.user.company.phone_number,
            address={"country": "FR"},
        )
        request.user.company.stripe_id = customer["id"]
        request.user.company.save()
    else:
        customer = stripe.Customer.retrieve(request.user.company.stripe_id)
    return customer


def find_product_type_by_offer(offer: Offer):
    if offer.name in ["A la carte", "Intermédiaire"]:
        product_type = "payment"
    else:
        product_type = "subscription"
    return product_type


def has_subscription(company: Company):
    pass
