import json
from datetime import date
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

from middleware import HttpRequestWithJob
from views_restrictions import company_required, finished_inscription_required

from data_management.models import Language, Profession, City, Quality

from students.models import Student
from matching.views import send_template_mail
from matching.models import Like, Chats
from welcome_pages.forms import EmailPoste, EmailForm

from companies.models import Job
from companies.forms import MissionForm, CandidatForm, JobForm
from companies.utils import filter_by_degree_level, get_matching_students


@company_required
@finished_inscription_required
# pylint: disable=unused-argument
def search_page(request: HttpRequestWithJob, **kwargs):
    assert request.user.company is not None
    return render(
        request,
        "companies/search.html",
        {
            "jobs": request.user.company.job_set.all(),
            "job": request.job,
        },
    )


@company_required
@finished_inscription_required
def student_card(request: HttpRequestWithJob):
    assert request.job is not None
    if not request.job.proposed_job:
        return HttpResponse(json.dumps([]), content_type="application/json")
    students = get_matching_students(request.job, request.GET)
    students = filter_by_degree_level(students, request.job)
    students = [student.get_card_infos() for student in students]
    return HttpResponse(
        json.dumps(students, ensure_ascii=False, default=str),
        content_type="application/json",
    )


@company_required
@finished_inscription_required
def change_research_mission(request: HttpRequestWithJob):
    context = {}
    context["job"] = request.job
    context["metiers"] = list(Profession.objects.values_list("profession", flat=True))
    if request.method == "POST":
        form = MissionForm(request.POST, instance=request.job)
        context["form"] = form
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("companies:change_research_candidat")
        messages.error(
            request, "Inscription échouée : veuillez vérifier vos informations."
        )

    else:
        context["form"] = MissionForm(instance=request.job)
    return render(request, "companies/change_research_mission.html", context)


@company_required
@finished_inscription_required
def change_research_candidat(request: HttpRequestWithJob):
    assert request.job is not None
    if request.method == "POST":
        form = CandidatForm(request.POST, instance=request.job)

        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont bien été pris en comptes !")
            return redirect("companies:search")
        messages.error(
            request,
            "Changements non pris en comptes : veuillez vérifier vos informations.",
        )

    else:
        form = CandidatForm(instance=request.job)
    return render(
        request,
        "companies/change_research_candidat.html",
        {
            "form": form,
            "qualities": request.job.qualities,
            "list_qualities": Quality.objects.all(),
            "langues": request.job.spoken_languages,
            "list_langues": Language.objects.all(),
            "job": request.job,
        },
    )


@company_required
@finished_inscription_required
def likes_page(request: HttpRequestWithJob):
    context = {}
    context["likes"] = Like.objects.filter(job=request.job)
    context["job"] = request.job
    return render(request, "companies/likes.html", context)


@company_required
@finished_inscription_required
def get_students_that_liked_job(request: HttpRequestWithJob):
    assert request.job is not None
    students_that_liked = Student.objects.filter(
        pk__in=request.job.like_set.filter(
            student_liked=True, company_liked=False
        ).values_list("student_id", flat=True)
    )
    students_as_dict = [student.get_card_infos() for student in students_that_liked]
    for student in students_as_dict:
        student["is_liked"] = False
    students_as_dict = json.dumps(students_as_dict, ensure_ascii=False, default=str)
    return HttpResponse(students_as_dict, content_type="application/json")


@company_required
@finished_inscription_required
def get_students_that_job_liked(request: HttpRequestWithJob):
    assert request.job is not None
    students_that_job_liked = Student.objects.filter(
        pk__in=list(
            request.job.like_set.filter(
                student_liked=False, company_liked=True
            ).values_list("student_id", flat=True)
        )
    )
    students_as_dict = [student.get_card_infos() for student in students_that_job_liked]
    for student in students_as_dict:
        student["is_liked"] = True

    students_as_dict = json.dumps(students_as_dict, ensure_ascii=False, default=str)
    return HttpResponse(students_as_dict, content_type="application/json")


@company_required
@finished_inscription_required
def matches_page(request: HttpRequestWithJob):
    return render(request, "companies/matches.html", {"job": request.job})


@company_required
@finished_inscription_required
def get_matches(request: HttpRequestWithJob):
    assert request.job is not None
    students_that_matched = Student.objects.filter(
        pk__in=request.job.like_set.filter(
            student_liked=True, company_liked=True
        ).values_list("student_id", flat=True)
    )
    students_as_dict = [student.get_card_infos() for student in students_that_matched]
    for student in students_as_dict:
        student["is_liked"] = True

    students_as_dict = json.dumps(students_as_dict, ensure_ascii=False, default=str)
    return HttpResponse(students_as_dict, content_type="application/json")


@company_required
@finished_inscription_required
def chat_page(request: HttpRequestWithJob):
    assert request.job is not None
    context = {}
    context["job"] = request.job
    context["students"] = []
    for like in request.job.like_set.filter(student_liked=True, company_liked=True):
        student = like.student
        photo = (
            f"/media/{student.photo}"
            if student.photo
            else "https://via.placeholder.com/80"
        )
        context["students"].append(
            [
                photo,
                student.pk,
                " ".join([student.first_name, student.last_name]),
            ]
        )
    return render(request, "companies/chat_page/_index.html", context)


@company_required
def delete_profil(request: HttpRequestWithJob):
    assert request.job is not None and request.user.company is not None
    request.job.delete()
    jobs = request.user.company.job_set.all()
    if not jobs:
        request.session.pop("job")
        job = Job(company=request.user.company)
        job.save()
        request.session["job"] = job.pk
        return redirect("companies:mission")
    request.session["job"] = jobs[0].pk
    return redirect("home:index")


@company_required
@finished_inscription_required
def get_student_infos_page(request: HttpRequestWithJob, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {}
    context["student"] = student
    context["age"] = relativedelta(date.today(), student.birthdate).years
    return render(request, "companies/student_infos.html", context)


@company_required
@finished_inscription_required
def create_job(request: HttpRequestWithJob):
    assert request.user.company is not None
    job = Job(company=request.user.company)
    job.save()
    request.session["job"] = job.pk
    return redirect("companies:mission")


@company_required
def mailMissingPoste(request: HttpRequestWithJob):
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
            messages.success(request, "Votre mail a bien été envoyé !")
        else:
            messages.error(request, "Le mail n'a pas été envoyé, veuillez réessayer.")
    return redirect("companies:mission")


@company_required
@finished_inscription_required
# pylint: disable=unused-argument
def researches(request: HttpRequestWithJob, **kargs):
    assert request.job is not None and request.user.company is not None
    context = {}
    context["job"] = request.job
    context["jobs"] = request.user.company.job_set.all()

    if request.method == "POST":
        context["form"] = JobForm(request.POST, instance=request.job)
        if context["form"].is_valid():
            context["form"].save()
            messages.success(request, "Les changements ont bien été pris en comptes !")

            return redirect("home:index")
        messages.error(request, "Erreur : veuillez vérifier vos informations.")

    else:
        context["form"] = JobForm(instance=request.job)

    context["form_mail"] = EmailPoste
    context["professions"] = list(
        Profession.objects.values_list("profession", flat=True)
    )
    context["cities"] = list(City.objects.values_list("city", flat=True))

    spoken_languages = request.job.spoken_languages or []
    chosen_qualities = request.job.qualities or []

    chosen_langs = []
    for language in spoken_languages:
        assert language is not None
        chosen_langs.append(language[0])

    context["all_qualities"] = list(Quality.objects.values_list("quality", flat=True))
    context["all_languages"] = list(Language.objects.values_list("language", flat=True))
    context["qualities"] = chosen_qualities
    context["spoken_languages"] = spoken_languages
    context["chosen_languages"] = chosen_langs
    context["professions"] = list(
        Profession.objects.values_list("profession", flat=True)
    )

    return render(request, "companies/researches.html", context)


@company_required
@finished_inscription_required
def send_message(request: HttpRequestWithJob):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    current_matches = list(
        Like.objects.filter(
            company_liked=True,
            student_liked=True,
            student_id=body["student_pk"],
            job_id=request.session["job"],
        ).values_list("student_id", flat=True)
    )

    if int(body["student_pk"]) not in current_matches:
        return HttpResponse(status=403)

    new_message = Chats(
        chat=body["chat"],
        job_id=request.session["job"],
        student_id=body["student_pk"],
        by="company",
    )
    new_message.save()
    send_template_mail(
        request,
        Student.objects.get(pk=body["student_pk"]).user.email,
        "mails/student/message.html",
        "Vous avez un message d'une entreprise sur leonework !",
    )
    return HttpResponse(status=202)
