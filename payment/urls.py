from django.urls import path


from . import views

app_name = "payment"

urlpatterns = [
    path("offres", views.offres, name="offres"),
    path("checkout", views.checkout, name="checkout"),
    path("compte", views.stripe_billings, name="compte"),
    path("success_checkout", views.success_checkout, name="success_checkout"),
    path("mailOffres", views.mailOffers, name="mailOffres"),
    path(
        "receive_payment_response",
        views.receive_payment_response,
        name="receive_payment_response",
    ),
    path(
        "invoice_request/<int:student_pk>/",
        views.invoice_request,
        name="invoice_request",
    ),
]
