from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from middleware import HttpRequestWithJob
from views_restrictions import (
    active_user_required,
    company_required,
)

from data_management.models import (
    CompanyValue,
    Language,
    Profession,
    City,
    Quality,
)

from welcome_pages.forms import EmailPoste
from matching.views import send_template_mail

from companies.forms import (
    IdentityForm,
    EntrepriseForm,
    MissionForm,
    CandidatForm,
    EngagementForm,
)
from companies.models import Company, Job


@active_user_required
@user_passes_test(lambda u: not u.is_student())
def identity(request: HttpRequestWithJob):
    status_code = 200

    # check if it's the first time the user is on this page
    if not hasattr(request.user, "company"):
        user_company = Company.objects.create(user=request.user)
        user_company.save()
        first_job = Job.objects.create(company=user_company)
        first_job.save()

    # handle the form submission
    if request.method == "POST":
        form = IdentityForm(request.POST, request.FILES, instance=request.user.company)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("companies:company")

        # form is not valid
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )
        status_code = 400
    else:
        form = IdentityForm(instance=request.user.company)
    return render(
        request,
        "companies/identity.html",
        {"form": form},
        status=status_code,
    )


@company_required
def mon_entreprise(request: HttpRequestWithJob):
    assert request.user.company is not None
    response_status = 200

    if request.method == "POST":
        form = EntrepriseForm(request.POST, instance=request.user.company)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("companies:mission")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )
        response_status = 400

    form = EntrepriseForm(instance=request.user.company)
    context = {
        "job": request.job,
        "form": form,
        "company_values": request.user.company.company_values,
        "all_values": list(CompanyValue.objects.values_list("value", flat=True)),
    }
    return render(
        request, "companies/mon_entreprise.html", context, status=response_status
    )


@company_required
def mission(request: HttpRequestWithJob):
    assert request.job is not None
    if request.user.finished_inscription and request.job.proposed_job:
        return redirect("home:index")
    response_status = 200
    if request.method == "POST":
        form = MissionForm(request.POST, instance=request.job)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("companies:candidat")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )
        response_status = 400

    else:
        form = MissionForm(instance=request.job)

    return render(
        request,
        "companies/mission.html",
        {
            "form": form,
            "job": request.job,
            "form_mail": EmailPoste,
            "professions": list(
                Profession.objects.values_list("profession", flat=True)
            ),
            "cities": list(City.objects.values_list("city", flat=True)),
        },
        status=response_status,
    )


@company_required
def candidat(request: HttpRequestWithJob):
    assert request.job is not None
    status_code = 200
    if request.method == "POST":
        form = CandidatForm(request.POST, instance=request.job)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            if request.user.finished_inscription:
                return redirect("home:index")
            return redirect("companies:engagement")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )
        status_code = 400
    else:
        form = CandidatForm(instance=request.job)

    return render(
        request,
        "companies/candidat.html",
        {
            "form": form,
            "qualities": request.job.qualities or [],
            "all_qualities": list(Quality.objects.values_list("quality", flat=True)),
            "spoken_languages": request.job.spoken_languages or [],
            "all_languages": list(Language.objects.values_list("language", flat=True)),
        },
        status=status_code,
    )


@company_required
def engagement(request: HttpRequestWithJob):
    assert request.job is not None
    status_code = 200
    if request.method == "POST":
        form = EngagementForm(request.POST, instance=request.user.company)
        if form.is_valid():
            if not form.cleaned_data["engagement"]:
                messages.error(
                    request, "Vous devez cocher la case pour valider votre inscription."
                )
            else:
                form.save()
                messages.success(
                    request, "Les changements ont bien été pris en comptes !"
                )
                if not request.user.finished_inscription:
                    send_template_mail(
                        request,
                        request.user.email,
                        "mails/company/welcome.html",
                        "Bienvenue sur leonework - la plateforme de matchmaking pour les étudiants"
                        + " / companies",
                    )
                    request.user.finished_inscription = True
                    request.user.save()

                return redirect("home:index")

        status_code = 400
    else:
        form = EngagementForm(instance=request.user.company)

    return render(
        request, "companies/engagement.html", {"form": form}, status=status_code
    )
