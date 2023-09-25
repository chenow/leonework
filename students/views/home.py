import json
from datetime import timedelta, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models.query import QuerySet
from data_management.models import City, CompanyValue, Domain, Profession


from middleware import HttpRequestWithJob

from companies.models import Job
from views_restrictions import student_required

from welcome_pages.forms import EmailMissingMetierForm
from matching.models import Like, Chats
from matching.views import send_template_mail

from ..forms import MissionForm, EntrepriseForm
from ..models import Student


@student_required
def search(request: HttpRequestWithJob):
    return render(request, "students/search.html")


@student_required
def change_research_mission(request: HttpRequestWithJob):
    assert request.user.student is not None
    if request.method == "POST":
        form = MissionForm(request.POST, instance=request.user.student)

        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("students:change_research_entreprise")
        messages.error(
            request,
            "Changements non pris en comptes : veuillez vérifier vos informations.",
        )

    else:
        form = MissionForm(instance=request.user.student)

    return render(
        request,
        "students/change_research_mission.html",
        {
            "form": form,
            "metiers": list(Profession.objects.values_list("professions", flat=True)),
            "domaines": list(Domain.objects.values_list("domain", flat=True)),
            "chosen_metiers": request.user.student.demanded_jobs,
            "chosen_domaines": request.user.student.demanded_domains,
            "form_mail": EmailMissingMetierForm(),
        },
    )


@student_required
def change_research_entreprise(request: HttpRequestWithJob):
    assert request.user.student is not None
    if request.method == "POST":
        form = EntrepriseForm(request.POST, instance=request.user.student)

        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("students:search")
        messages.error(
            request,
            "Changements non pris en comptes : veuillez vérifier vos informations.",
        )

    else:
        form = EntrepriseForm(instance=request.user.student)
    return render(
        request,
        "students/change_research_entreprise.html",
        {
            "form": form,
            "url": "students:change_research_entreprise",
            "metiers": list(Profession.objects.values_list("professions", flat=True)),
            "domaines": list(Domain.objects.values_list("domain", flat=True)),
            "chosen_metiers": request.user.student.demanded_jobs,
            "valeurs": CompanyValue.objects.all(),
            "cities": City.objects.all(),
            "chosen_domaines": request.user.student.demanded_domains,
            "form_mail": EmailMissingMetierForm(),
        },
    )


@student_required
def entreprise_card(request: HttpRequestWithJob):
    assert request.user.student is not None
    if request.GET.get("matchingOndomaine") == "false":
        metiers_recherches = request.user.student.demanded_jobs

    else:
        domains = []
        for domain in request.user.student.demanded_domains:
            domains.append(Domain.objects.get(domain=domain).pk)
        metiers_recherches = list(
            Profession.objects.filter(domain__in=domains).values_list(
                "profession", flat=True
            )
        )
        for metier in request.user.student.demanded_jobs:
            metiers_recherches.append(metier)

    jobs = Job.objects.filter(proposed_job__in=metiers_recherches)
    jobs = jobs.filter(contract_type=request.user.student.contract_type)
    jobs = jobs.filter(qualities__overlap=request.user.student.qualities)
    for job in jobs:
        if not bool(
            set(job.company.overall_atmospheres)
            & set(request.user.student.overall_atmospheres)
        ):
            jobs = jobs.exclude(id=job.pk)
        if not bool(
            set(job.company.company_values) & set(request.user.student.company_values)
        ):
            jobs = jobs.exclude(id=job.pk)
        if not bool(
            set([job.company.company_size]) & set(request.user.student.company_sizes)
        ):
            jobs = jobs.exclude(pk=job.pk)
    datedebutmission = request.GET.get("DateDebutMission")
    if datedebutmission is None:
        datedebutmission = datetime.today().strftime("%d/%m/%Y")
    jobs = jobs.filter(
        beginning_date__range=[
            datetime.strptime(datedebutmission, "%d/%m/%Y") - timedelta(days=31 * 3),
            datetime.strptime(datedebutmission, "%d/%m/%Y") + timedelta(days=31 * 3),
        ],
    )
    encadrement = request.GET.get("matchingOnEncadrement", "").split(",")
    jobs = jobs.filter(autonomy__overlap=encadrement)

    if request.GET.get("matchingOnWeekend") == "samedi":
        jobs = jobs.filter(work_weekend__in=["samedi", "les_deux", "False"])
    elif request.GET.get("matchingOnWeekend") == "dimanche":
        jobs = jobs.filter(work_weekend__in=["dimanche", "les_deux", "False"])
    elif request.GET.get("matchingOnWeekend") == "les_deux":
        pass
    elif request.GET.get("matchingOnWeekend") == "False":
        jobs = jobs.filter(work_weekend="False")

    if request.GET.get("matchingOnteleworking") == "None":
        pass

    else:
        for job in jobs:
            if job.teleworking not in [
                "None",
                request.GET.get("matchingOnteleworking"),
            ]:
                jobs = jobs.exclude(id=job.pk)

    if request.GET.get("matchingOnDepartement") == "false":
        jobs = jobs.filter(job_location__in=request.user.student.company_locations)
    else:
        job_location = []
        for city in request.user.student.company_locations:
            region = City.objects.get(city=city).region
            for i in City.objects.filter(region=region):
                job_location.append(i.city)
        jobs = jobs.filter(job_location__in=job_location)
    jobs = filter_by_degree_level_student(jobs, request.user.student)
    for job in jobs:
        if job.pk in request.user.student.like_set.filter(
            student_liked=True
        ).values_list("job", flat=True):
            jobs.remove(job)

    jobs = [job.get_job_infos() for job in jobs]
    for job in jobs:
        job["is_liked"] = False

    jobs = json.dumps(jobs, ensure_ascii=False, default=str)
    return HttpResponse(jobs, content_type="application/json")


@student_required
def change_search(request: HttpRequestWithJob):
    return render(request, "students/change_search.html")


@student_required
def likes(request: HttpRequestWithJob):
    context = {}
    context["likes"] = Like.objects.filter(student=request.user.student)
    return render(request, "students/likes.html", context)


@student_required
def get_jobs_that_student_liked(request: HttpRequestWithJob):
    assert request.user.student is not None
    jobs_that_student_liked = Job.objects.filter(
        pk__in=list(
            request.user.student.like_set.filter(
                student_liked=True, company_liked=False
            ).values_list("job_id", flat=True)
        )
    )
    jobs_that_student_liked = [job.get_job_infos() for job in jobs_that_student_liked]
    jobs_that_student_liked = json.dumps(
        jobs_that_student_liked, ensure_ascii=False, default=str
    )
    return HttpResponse(jobs_that_student_liked, content_type="application/json")


@student_required
def get_jobs_that_liked_student(request: HttpRequestWithJob):
    assert request.user.student is not None
    jobs_that_liked_student = Job.objects.filter(
        pk__in=list(
            request.user.student.like_set.filter(
                student_liked=False, company_liked=True
            ).values_list("job_id", flat=True)
        )
    )
    jobs_that_liked_student = [job.get_job_infos() for job in jobs_that_liked_student]
    jobs_that_liked_student = json.dumps(
        jobs_that_liked_student, ensure_ascii=False, default=str
    )
    return HttpResponse(jobs_that_liked_student, content_type="application/json")


@student_required
def matches(request: HttpRequestWithJob):
    return render(request, "students/matches.html")


@student_required
def get_matches(request: HttpRequestWithJob):
    assert request.user.student is not None
    jobs_that_matched_with_student = Job.objects.filter(
        pk__in=list(
            request.user.student.like_set.filter(
                student_liked=True, company_liked=True
            ).values_list("job_id", flat=True)
        )
    )
    jobs_that_matched_with_student = [
        job.get_job_infos() for job in jobs_that_matched_with_student
    ]
    jobs_that_matched_with_student = json.dumps(
        jobs_that_matched_with_student, ensure_ascii=False, default=str
    )
    return HttpResponse(jobs_that_matched_with_student, content_type="application/json")


@student_required
def chat(request: HttpRequestWithJob):
    context = {}
    context["student"] = request.user.student
    context["jobs"] = []
    for job in list(
        Like.objects.filter(
            student=request.user.student, company_liked=True, student_liked=True
        ).values("job")
    ):
        job_bdd = Job.objects.get(pk=job["job"])
        if job_bdd.company.photo == "":
            photo = "https://via.placeholder.com/80"
        else:
            photo = f"/media/{job_bdd.company.photo}"
        context["jobs"].append([photo, job["job"], job_bdd.company.name])
    return render(request, "students/messages.html", context)


@student_required
def get_company_infos(request, pk):
    job = get_object_or_404(Job, pk=pk)
    context = {}
    context["job"] = job
    context["company"] = job.company
    return render(request, "students/company_infos.html", context)


@student_required
def delete_profil(request: HttpRequestWithJob):
    assert request.user.student is not None
    request.user.student.delete()
    request.user.finished_inscription = False
    request.user.company_or_student = None
    request.user.save()
    return redirect("home:index")


@student_required
def send_message(request: HttpRequestWithJob):
    assert request.user.student is not None
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    likes_ids = list(
        Like.objects.filter(
            company_liked=True,
            student_liked=True,
            student_id=request.user.student.pk,
            job_id=body["job_pk"],
        ).values_list("job_id", flat=True)
    )

    if int(body["job_pk"]) not in likes_ids:
        return HttpResponse(status=403)
    new_chat = Chats(
        chat=body["chat"],
        job_id=body["job_pk"],
        student_id=request.user.student.pk,
        by="student",
    )
    new_chat.save()
    send_template_mail(
        request,
        Job.objects.get(pk=body["job_pk"]).company.user.email,
        "mails/company/message.html",
        "Vous avez un message d’un étudiant sur leonework",
    )
    return HttpResponse(status=202)


def filter_by_degree_level_student(jobs: QuerySet[Job], student: Student) -> list[Job]:
    order = {
        "pro": {},
        "bac": {},
        "university": {},
        "ingenieur": {},
        "art": {},
        "dcg": {},
    }

    order["pro"] = {
        "niveau 1": [
            "CAP - 1ère année",
            "CAP - 2ème année",
            "BP - 1ère année",
            "BP - 2ème année",
            "BAC PRO - 1ère année",
            "BAC PRO - 2ème année",
        ],
        "niveau 2": [
            "CAP - 2ème année",
            "BP - 1ère année",
            "BP - 2ème année",
            "BAC PRO - 2ème année",
        ],
        "niveau 3": [
            "BP - 1ère année",
            "BP - 2ème année",
            "BAC PRO - 2ème année",
        ],
        "niveau 4": [
            "BP - 2ème année",
            "BAC PRO - 2ème année",
        ],
    }

    order["bac"] = {
        "niveau 1": [
            "BAC PRO - 1ère année",
            "BAC PRO - 2ème année",
            "BTS - 1ère année",
            "BTS - 2ème année",
            "DEUST - 1ère année",
            "DEUST - 2ème année",
        ],
        "niveau 2": [
            "BAC PRO - 2ème année",
            "BTS - 1ère année",
            "BTS - 2ème année",
            "DEUST - 1ère année",
            "DEUST - 2ème année",
        ],
        "niveau 3": [
            "BAC PRO - 2ème année",
            "BTS - 2ème année",
            "DEUST - 2ème année",
        ],
    }
    order["university"] = {
        "niveau 1": [
            "Licence Professionnelle - 1ère année",
            "Licence Professionnelle - 2ème année",
            "Licence Professionnelle - 3ème année",
            "LICENCE - 1ère année",
            "LICENCE - 2ème année",
            "LICENCE - 3ème année",
            "BACHELOR - 1ère année",
            "BACHELOR - 2ème année",
            "BACHELOR - 3ème année",
            "BUT - 1ère année",
            "BUT - 2ème année",
            "BUT - 3ème année",
            "Titre ingénieur - 1ère année",
            "Titre ingénieur - 2ème année",
            "Titre ingénieur - 3ème année",
            "MBA - 1ère année",
            "MBA - 2ème année",
            "MASTER - 1ère année",
            "MASTER - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
        ],
        "niveau 2": [
            "Licence Professionnelle - 2ème année",
            "Licence Professionnelle - 3ème année",
            "LICENCE - 2ème année",
            "LICENCE - 3ème année",
            "BACHELOR - 2ème année",
            "BACHELOR - 3ème année",
            "BUT - 2ème année",
            "BUT - 3ème année",
            "Titre ingénieur - 2ème année",
            "Titre ingénieur - 3ème année",
            "MBA - 1ère année",
            "MBA - 2ème année",
            "MASTER - 1ère année",
            "MASTER - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
        ],
        "niveau 3": [
            "Licence Professionnelle - 3ème année",
            "LICENCE - 3ème année",
            "BACHELOR - 3ème année",
            "BUT - 3ème année",
            "Titre ingénieur - 3ème année",
            "MBA - 1ère année",
            "MBA - 2ème année",
            "MASTER - 1ère année",
            "MASTER - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
        ],
        "niveau 4": [
            "MBA - 1ère année",
            "MBA - 2ème année",
            "MASTER - 1ère année",
            "MASTER - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
            "Titre ingénieur - 3ème année",
        ],
        "niveau 5 :": [
            "Titre ingénieur - 3ème année",
            "MBA - 2ème année",
            "MASTER - 2ème année",
            "MS - 2ème année",
        ],
    }
    order["art"] = {
        "niveau 1": [
            "DMA - 1ère année",
            "DMA - 2ème année",
        ],
        "niveau 2": [
            "DMA - 2ème année",
        ],
    }

    order["dcg"] = {
        "niveau 1": [
            "DCG - 1ère année",
            "DCG - 2ème année",
            "DCG - 3ème année",
            "dscg - 1ère année",
            "dscg - 2ème année",
        ],
        "niveau 2": [
            "DCG - 2ème année",
            "DCG - 3ème année",
            "dscg - 1ère année",
            "dscg - 2ème année",
        ],
        "niveau 3": [
            "DCG - 3ème année",
            "dscg - 1ère année",
            "dscg - 2ème année",
        ],
        "niveau 4": [
            "dscg - 1ère année",
            "dscg - 2ème année",
        ],
        "niveau 5": [
            "dscg - 2ème année",
        ],
    }
    jobs_filtered = []
    # student_level = (
    #     f"{Degree.objects.filter(subject=student.ongoing_degree.replace('.', '')).level}"
    #     " - "
    #     f"{student.ongoing_year}"
    # )

    # for job in jobs:
    #     filtre = ""
    #     for _, levels in order.items():
    #         for level, diplomes in levels.items():
    #             if job.minimal_degree in diplomes:
    #                 filtre = levels[level]

    #     if student_level in filtre:
    #         jobs_filtered.append(job)
    return list(jobs)
