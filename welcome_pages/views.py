from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.views.defaults import server_error

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import EmailMessage

from middleware import HttpRequestWithJob
from welcome_pages.models import User

from .mails import account_activation_token
from .forms import AcceuilForm, LoginForm, NewUserForm, NewLinkForm


def presentation(request: HttpRequestWithJob):
    return render(request, "welcome_pages/home.html")


def mentions_legales(request: HttpRequestWithJob):
    return render(request, "welcome_pages/mentions_legales.html")


def cookies(request: HttpRequestWithJob):
    return render(request, "welcome_pages/cookies.html")


def confidentialite(request: HttpRequestWithJob):
    return render(request, "welcome_pages/confidentialite.html")


def cgv(request: HttpRequestWithJob):
    return render(request, "welcome_pages/cgv.html")


def cgu(request: HttpRequestWithJob):
    return render(request, "welcome_pages/cgu.html")


# register views


def delete_account(request: HttpRequestWithJob):
    if request.method == "POST":
        request.user.delete()
        return redirect("home:index")
    return render(request, "welcome_pages/delete_account.html")


def register(request: HttpRequestWithJob):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data["password"])
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))
            login(request, user)
            messages.success(
                request,
                (
                    "Vous êtes désormais bien inscrit.e ! Veuillez vous "
                    f"rendre sur votre boîte mail {user.email} afin de cliquer"
                    " sur le lien de validation dans le mail que nous venons de vous envoyer."
                ),
            )
            return redirect("home:index")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )

    else:
        form = NewUserForm()
    return render(request, "welcome_pages/register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user: User
        user.is_active = True
        user.save()

        messages.success(
            request,
            (
                "Merci d'avoir validé votre email."
                "Vous pouvez désormais vous connecter pour poursuivre l'inscription."
            ),
        )
        return redirect("welcome_pages:login")
    messages.error(
        request,
        "Le lien d'activation est invalide ! Veuillez en redemander un nouveau.",
    )
    return redirect("welcome_pages:login")


@login_required
def waiting_mail_check(request: HttpRequestWithJob):
    if request.method == "POST":
        form = NewLinkForm(request.POST)
        if form.is_valid():
            try:
                user: User = User.objects.get(email=form.cleaned_data.get("email"))
            except User.DoesNotExist:
                messages.error(
                    request,
                    f"Le mail {form.cleaned_data.get('email')} ne correspond à aucun profil.",
                )
                return redirect("home:index")
            activateEmail(request, user, form.cleaned_data.get("email"))
            messages.success(
                request,
                f"Nous venons de renvoyer un mail d'activation à {user.email}.",
            )
            return redirect("home:index")
        messages.error(request, "Mail non envoyé : veuillez vérifier vos informations.")

    else:
        form = NewLinkForm()
    return render(request, "welcome_pages/waiting_mail_check.html", {"form": form})


def activateEmail(request: HttpRequestWithJob, user: User, to_email):
    mail_subject = "Activation de votre compte Leonework"
    message = render_to_string(
        "mails/email_verification.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        pass
    else:
        messages.error(
            request,
            f"Nous n'avons pas réussi à envoyer de mail de confirmation) à {to_email}, "
            + "veuillez réessayer de vous inscrire.",
        )


def own_login(request: HttpRequestWithJob):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect("home:index")
            messages.error(
                request,
                "Connexion échouée : veuillez vérifiez votre adresse mail et mot de passe.",
            )
            return redirect("home:index")

    else:
        form = LoginForm()
    return render(request, "welcome_pages/login.html", {"form": form})


@login_required
def own_logout(request: HttpRequestWithJob):
    logout(request)
    messages.success(request, "Vous vous êtes bien déconnecté.e !")
    return render(request, "welcome_pages/home.html")


@login_required
@user_passes_test(lambda u: u.is_active)
def beginning_inscription(request: HttpRequestWithJob):
    if not hasattr(request.user, "student") and not hasattr(request.user, "company"):
        return render(request, "welcome_pages/beginning_inscription.html")
    return redirect("home:identity")


def error_404_view(request, exception):
    return render(request, "generic/error404.html")


def error_500_view(request):
    return server_error(request, template_name="generic/error500.html")


def mailAcceuil(request: HttpRequestWithJob):
    if request.method == "POST":
        form = AcceuilForm(request.POST)
        if form.is_valid():
            mail = EmailMultiAlternatives(
                "[Leonework] " + form.cleaned_data["object"],
                form.cleaned_data["message"],
                f'"{form.cleaned_data["email"]}" <{form.cleaned_data["email"]}>',
                ["audrey@leonework.com"],
                reply_to=[form.cleaned_data["email"]],
            )
            mail.send()
            messages.success(request, "Votre mail de contact a bien été envoyé !")
        else:
            messages.error(request, "Le mail n'a pas été envoyé, veuillez réessayer.")
    return redirect("welcome_pages:presentation")
