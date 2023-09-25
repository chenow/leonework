from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from middleware import HttpRequestWithJob

from welcome_pages.forms import EmailForm, EmailMissingMetierForm


@login_required
def mailMissingDiplome(request: HttpRequestWithJob):
    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid():
            mail = EmailMultiAlternatives(
                "[Leonework] " + form.cleaned_data["object"],
                form.cleaned_data["message"],
                f'"{request.user.email}" <{request.user.email}>',
                ["audrey@leonework.com"],
                reply_to=[request.user.email],
            )
            mail.send()
            messages.success(
                request,
                "Votre mail pour demander à rajouter une formation a bien été envoyé !",
            )
        else:
            messages.error(request, "Le mail n'a pas été envoyé, veuillez réessayer.")
    return redirect("students:parcours")


@login_required
def mailMissingMetier(request: HttpRequestWithJob):
    if request.method == "POST":
        form = EmailMissingMetierForm(request.POST)

        if form.is_valid():
            mail = EmailMultiAlternatives(
                "[Leonework] " + form.cleaned_data["object"],
                form.cleaned_data["message"],
                f'"{request.user.email}" <{request.user.email}>',
                ["audrey@leonework.com"],
                reply_to=[request.user.email],
            )
            mail.send()
            messages.success(
                request,
                "Votre mail pour demander à rajouter une formation a bien été envoyé !",
            )
        else:
            messages.error(request, "Le mail n'a pas été envoyé, veuillez réessayer.")
    return redirect("students:mission")
