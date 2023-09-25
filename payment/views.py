import html

import stripe

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib import messages
from django.contrib.auth import login
from django.utils.html import strip_tags


from _conf.settings import STRIPE_PK, CHECKOUT_RESPONSE_KEY, DEFAULT_DOMAIN
from companies.models import Company
from middleware import HttpRequestWithJob
from students.models import Student
from views_restrictions import company_required
from welcome_pages.models import User

from .forms import EmailOffersForm
from .models import Subscription, Offer
from .utils import find_or_create_stripe_customer


stripe.api_key = STRIPE_PK
endpoint_secret = CHECKOUT_RESPONSE_KEY


def offres(request: HttpRequestWithJob):
    offers = Offer.objects.filter(active=True)
    return render(request, "stripe/offres.html", {"offers": offers})


@company_required
def checkout(request: HttpRequestWithJob):
    assert request.user.company is not None
    price_id = "price_1NOkpKD4Z8VaXSKtDk95EYQT"
    customer = find_or_create_stripe_customer(request)

    success_url = (
        DEFAULT_DOMAIN
        + reverse("payment:success_checkout")
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = DEFAULT_DOMAIN + reverse("companies:search")

    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        mode="payment",
        customer=customer["id"],
        line_items=[{"price": price_id, "quantity": 1}],
        customer_update={
            "address": "auto",
        },
        automatic_tax={
            "enabled": True,
        },
        client_reference_id=str(request.user.pk),
    )
    return redirect(session.url)


@company_required
def invoice_request(request: HttpRequestWithJob, student_pk: int):
    student = Student.objects.get(pk=student_pk)
    like_id = student.like_set.filter(job=request.job).first().pk
    html_message = (
        "Suite à un recrutement effectué sur la plateforme Léonework, "
        + f"l'entreprise {request.user.company.name} ({request.user.email}) "
        + f"demande une facture pour le recrutement de {student.first_name} "
        + f"{student.last_name} ({student.user.email}).<br><br>"
        + "les détails des deux profils sont disponibles sur la plateforme à l'url suivante : "
        + f"<a href='https://leonework.com/administration/matching/like/{like_id}/'>"
        + f"https://leonework.com/companies/matching/like//{like_id}/</a>"
    )

    message = strip_tags(html.unescape(html_message))

    send_mail(
        "[Léonework] - Demande de facture",
        message,
        "no-reply@leonework.com",
        ["audrey@leonework.com", "antoine.cheneau@student-cs.fr"],
        html_message=html_message,
    )

    messages.success(
        request,
        "Votre demande de facture a bien été envoyée suite au recrutement "
        + f"de {student.first_name} {student.last_name} ! "
        + "Nous allons vous envoyer sous peu la facture correspondante par mail.",
    )
    return redirect("companies:search")


def success_checkout(request: HttpRequestWithJob):
    session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    user = Company.objects.get(stripe_id=session["customer"]).user
    login(request, user)
    assert user.company is not None
    request.session["job"] = user.company.job_set.all()[0].pk
    messages.success(
        request, "Paiement réussi, nous vous remercions de votre confiance."
    )
    return redirect("home:index")


@company_required
def stripe_billings(request: HttpRequestWithJob):
    assert request.user.company is not None
    return_url = DEFAULT_DOMAIN + reverse("home:index")
    portal = stripe.billing_portal.Configuration.create(
        features={
            "customer_update": {
                "allowed_updates": [
                    "email",
                ],
                "enabled": True,
            },
            "invoice_history": {"enabled": True},
            "payment_method_update": {"enabled": True},
        },
        business_profile={
            "privacy_policy_url": "https://leonework.com/confidentialite",
            "terms_of_service_url": "https://leonework.com/cgu",
        },
    )
    portalSession = stripe.billing_portal.Session.create(
        customer=request.user.company.stripe_id,
        configuration=portal.id,
        return_url=return_url,
        locale="fr",
    )
    return redirect(portalSession.url)


@csrf_exempt
def receive_payment_response(request: HttpRequestWithJob):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    # pylint: disable=unused-variable
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:  # type: ignore
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user: User = User.objects.get(pk=session["client_reference_id"])
        assert user.company is not None

        if session["payment_status"] == "paid":
            send_mail(
                "Paiement réussi",
                "Suite à un recrutement effectué sur la plateforme Léonework, "
                + f"le paiement de {user.company.name} ({user.email}) a été "
                + "effectué avec succès via Stripe.",
                "no-reply@leonework.com",
                ["audrey@leonework.com", "antoine.cheneau@student-cs.fr"],
                fail_silently=False,
            )

        return HttpResponse(status=200)

    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
        send_mail(
            "Paiement réussi",
            "Suite à un recrutement effectué sur la plateforme Léonework, "
            + f"le paiement de {user.company.name} ({user.email}) "
            + "a bien été réceptionné sur le compte Stripe.",
            "no-reply@leonework.com",
            ["audrey@leonework.com", "antoine.cheneau@student-cs.fr"],
            fail_silently=False,
        )
        return HttpResponse(status=200)

    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]
        subscription = Subscription.objects.get(pk=session.client_reference_id)
        subscription.payment_status = "error"
        subscription.save()
        send_mail(
            "Paiement réussi",
            "Suite à un recrutement effectué sur la plateforme Léonework, "
            + f"L'entreprise {user.company.name} ({user.email}) a essayé de "
            + "payer Léonework par stripe"
            + "mais le paiement n'est pas passé.",
            "no-reply@leonework.com",
            ["audrey@leonework.com", "antoine.cheneau@student-cs.fr"],
            fail_silently=False,
        )

    # Passed signature verification
    return HttpResponse(status=200)


@login_required
def mailOffers(request: HttpRequestWithJob):
    if request.method == "POST":
        form = EmailOffersForm(request.POST)
        if form.is_valid():
            mail = EmailMultiAlternatives(
                "[Leonework] " + form.cleaned_data["object"],
                form.cleaned_data["message"],
                f'"{request.user.email}" <{request.user.email}>',
                ["audrey@leonework.com"],
                reply_to=[request.user.email],
            )
            mail.send()
            messages.success(request, "Votre mail de contact a bien été envoyé !")
        else:
            messages.error(request, "Le mail n'a pas été envoyé, veuillez réessayer.")
    return redirect("payment:offres")
