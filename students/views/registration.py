from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


from middleware import HttpRequestWithJob

from data_management.models import (
    CompanyValue,
    Degree,
    Domain,
    Language,
    Profession,
    City,
    Quality,
)
from views_restrictions import student_required

from welcome_pages.forms import EmailForm, EmailMissingMetierForm
from matching.views import send_template_mail

from ..forms import AtoutsForm, EntrepriseForm, IdentityForm, MissionForm, ParcoursForm
from ..models import Student


@user_passes_test(lambda user: user.is_active)
def identity(request: HttpRequestWithJob):
    if not request.user.is_student():
        request.user.student = Student.objects.create(user=request.user)
        request.user.student.save()

    if request.method == "POST":
        form = IdentityForm(request.POST, request.FILES, instance=request.user.student)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("students:parcours")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )
    else:
        form = IdentityForm(instance=request.user.student)
    return render(
        request,
        "students/identity.html",
        {"form": form},
    )


@student_required
def parcours(request: HttpRequestWithJob):
    assert request.user.student is not None
    if request.method == "POST":
        form = ParcoursForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("students:atouts")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )
    else:
        form = ParcoursForm(instance=request.user.student)
    form_mail = EmailForm()
    all_degrees = [
        f"{degree.level} - {degree.subject}" for degree in Degree.objects.all()
    ]
    return render(
        request,
        "students/parcours.html",
        {
            "form": form,
            "form_mail": form_mail,
            "experiences": request.user.student.experiences,
            "all_degrees": all_degrees,
        },
    )


@student_required
def atouts(request: HttpRequestWithJob):
    assert request.user.student is not None
    if request.method == "POST":
        form = AtoutsForm(request.POST, instance=request.user.student)

        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("students:mission")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )

    else:
        form = AtoutsForm(instance=request.user.student)
    context = {}
    context["form"] = form

    spoken_languages = request.user.student.spoken_languages or []
    qualities = request.user.student.qualities or []

    chosen_languages = []
    for language in spoken_languages:
        chosen_languages.append(language[0])

    context["qualities"] = qualities
    context["spoken_languages"] = spoken_languages
    context["chosen_languages"] = chosen_languages
    context["all_qualities"] = Quality.objects.values_list("quality", flat=True)
    context["all_languages"] = Language.objects.values_list("language", flat=True)
    return render(request, "students/atouts.html", context)


@student_required
def mission(request: HttpRequestWithJob):
    assert request.user.student is not None
    if request.method == "POST":
        form = MissionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if (
                not form.cleaned_data["demanded_domains"]
                and not form.cleaned_data["demanded_jobs"]
            ):
                messages.error(
                    request,
                    "Veuillez saisir au moins un métier ou un domaine recherché.",
                )
            else:
                form.save()
                messages.success(
                    request, "Les changements ont bien été pris en comptes !"
                )
                return redirect("students:company")
        else:
            messages.error(
                request, "Inscription échouée : veuillez vérifier vos informations."
            )

    else:
        form = MissionForm(instance=request.user.student)
    return render(
        request,
        "students/mission.html",
        {
            "form": form,
            "professions": list(
                Profession.objects.values_list("profession", flat=True)
            ),
            "domains": list(Domain.objects.values_list("domain", flat=True)),
            "demanded_jobs": request.user.student.demanded_jobs,
            "demanded_domains": request.user.student.demanded_domains,
            "form_mail": EmailMissingMetierForm(),
        },
    )


@student_required
def company(request: HttpRequestWithJob):
    assert request.user.student is not None
    if request.method == "POST":
        form = EntrepriseForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if not request.user.student.company_locations:
                messages.error(request, "Veuillez saisir au moins une ville.")
            elif not request.user.student.company_values:
                messages.error(request, "Veuillez saisir au moins une valeur.")
            else:
                form.save()
                messages.success(
                    request,
                    (
                        "Les changements ont bien été pris en comptes ! "
                        "Votre inscription est terminée."
                    ),
                )
                if not request.user.finished_inscription:
                    send_template_mail(
                        request,
                        request.user.email,
                        "mails/student/welcome.html",
                        (
                            "Bienvenue sur leonework - "
                            "la plateforme de matchmaking pour les étudiants / entreprises"
                        ),
                    )

                request.user.finished_inscription = True
                request.user.save()
                return redirect("home:index")
        else:
            messages.error(
                request, "Inscription échouée : veuillez vérifier vos informations."
            )

    else:
        form = EntrepriseForm(instance=request.user.student)
    return render(
        request,
        "students/entreprise.html",
        {
            "form": form,
            "company_values": request.user.student.company_values or [],
            "chosen_cities": request.user.student.company_locations or [],
            "all_values": list(CompanyValue.objects.values_list("value", flat=True)),
            "cities": list(City.objects.values_list("city", flat=True)),
        },
    )
