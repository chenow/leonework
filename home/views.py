from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives

from middleware import HttpRequestWithJob
from .forms import EmailSupportForm


def index(request: HttpRequestWithJob):
    if not request.user.is_authenticated:
        return render(request, "welcome_pages/home.html")
    if not request.user.is_active:
        return redirect("welcome_pages:waiting_mail_check")
    if not request.user.finished_inscription:
        return redirect("welcome_pages:beginning_inscription")
    if request.user.is_student():
        return redirect("students:search")
    if request.user.is_company():
        return redirect("companies:search")

    # if user goes here there is a bug
    return render(request, "welcome_pages/home.html")


def change_search(request: HttpRequestWithJob):
    if request.user.is_company():
        return redirect("companies:identity")
    elif request.user.is_student():
        return redirect("students:identity")
    return redirect("welcome_pages:beginning_inscription")


def likes(request: HttpRequestWithJob):
    if request.user.is_company():
        return redirect("companies:likes")
    elif request.user.is_student():
        return redirect("students:likes")
    return redirect("welcome_pages:beginning_inscription")


def matches(request: HttpRequestWithJob):
    if request.user.is_company():
        return redirect("companies:matches")
    elif request.user.is_student():
        return redirect("students:matches")
    return redirect("welcome_pages:beginning_inscription")


def message(request: HttpRequestWithJob):
    if request.user.is_company():
        return redirect("companies:message")
    elif request.user.is_student():
        return redirect("students:message")
    return redirect("welcome_pages:beginning_inscription")


@login_required
def faq(request: HttpRequestWithJob):
    return render(request, "home/faq.html")


@login_required
def support(request: HttpRequestWithJob):
    if request.method == "POST":
        form = EmailSupportForm(request.POST)

        if form.is_valid():
            mail = EmailMultiAlternatives(
                "[Leonework] " + form.cleaned_data["object"],
                form.cleaned_data["message"],
                f'"{request.user.email}" <{request.user.email}>',
                ["audrey@leonework.com"],
                reply_to=[request.user.email],
            )
            mail.send()
            messages.success(request, "Votre mail a bien été envoyé !")
            return redirect("home:index")

        messages.error(request, "Le mail n'a pas été envoyé, veuillez réessayer.")
    else:
        form = EmailSupportForm()
    return render(request, "home/support.html", {"form": form})


@login_required
def identity(request: HttpRequestWithJob):
    if request.user.is_company():
        return redirect("companies:identity")
    elif request.user.is_student():
        return redirect("students:identity")
    return redirect("welcome_pages:beginning_inscription")
