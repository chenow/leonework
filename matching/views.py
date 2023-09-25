import json

from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from data_management.models import Profession

from middleware import HttpRequestWithJob

from students.models import Student
from companies.models import Company, Job
from views_restrictions import finished_inscription_required

from .models import Like, Chats


@finished_inscription_required  # type : ignore
def create_like(request: HttpRequestWithJob, pk):
    job = Job.objects.get(pk=pk)
    try:
        like = request.user.student.like_set.get(job=job)
        if like.student_liked and not like.company_liked:  # only student liked
            like.student_liked = False
            like.save()
            like.delete()
        elif (
            like.student_liked and like.company_liked
        ):  # both student and company liked
            like.student_liked = False
            like.save()
        else:  # only company liked before
            like.student_liked = True
            like.save()
    except:
        like = Like(student=request.user.student, job=job)
        like.student_liked = True
        like.save()
    if like.company_liked and like.student_liked:
        send_template_mail(
            request,
            request.user.student.user.email,
            "mails/student/match.html",
            "Félicitations ! Vous avez un nouveau match sur Leonework",
        )
        send_template_mail(
            request,
            job.company.user.email,
            "mails/company/match.html",
            "Match avec un étudiant!",
        )
    elif like.student_liked:
        send_template_mail(
            request,
            job.company.user.email,
            "mails/company/like.html",
            "Un étudiant a liké votre company !",
        )
    return HttpResponse()


@finished_inscription_required
def create_like_company(request: HttpRequestWithJob, student_pk):
    job = Job.objects.get(pk=request.session.get("job"))
    student = Student.objects.get(pk=student_pk)
    try:
        like = job.like_set.get(student=student)
        if like.company_liked and not like.student_liked:  # only company liked
            like.company_liked = False
            like.save()
            like.delete()
        elif (
            like.student_liked and like.company_liked
        ):  # both company and company liked
            like.company_liked = False
            like.save()
        else:  # only student liked before
            like.company_liked = True
            like.save()
    except:
        like = Like(student=student, job=job)
        like.company_liked = True
        like.save()
    if like.student_liked and like.company_liked:
        send_template_mail(
            request,
            student.user.email,
            "mails/student/match.html",
            "Félicitations ! Vous avez un nouveau match sur Leonework",
        )
        send_template_mail(
            request,
            job.company.user.email,
            "mails/company/match.html",
            "Match avec un étudiant!",
        )
    elif like.company_liked:
        send_template_mail(
            request,
            student.user.email,
            "mails/student/like.html",
            "Vous avez reçu un like sur Leonework !",
        )
    return HttpResponse()


@finished_inscription_required
def get_messages(request: HttpRequestWithJob, user_type, pk):
    chats_list = []
    if user_type == "company":
        like = Like.objects.filter(student=pk, job=request.session.get("job")).first()
    else:
        like = Like.objects.filter(student=request.user.student, job=pk).first()
    if like is None:
        return HttpResponse(status=403)
    if not like.student_liked and like.company_liked:
        return HttpResponse(status=404)

    if user_type == "company":
        chats = Chats.objects.filter(
            student=pk, job=request.session.get("job")
        ).order_by("date")
    else:
        chats = Chats.objects.filter(student=request.user.student, job=pk).order_by(
            "date"
        )
    for chat in chats:
        chats_list.append([chat.chat, chat.date.strftime("%d/%m/%Y - %H:%M"), chat.by])
    chats = json.dumps(chats_list, ensure_ascii=False, default=str)
    return HttpResponse(chats, content_type="application/json")


@finished_inscription_required
# pylint: disable=unused-argument
def get_card_infos(request: HttpRequestWithJob, pk, user_type):
    if user_type == "job":
        job = Job.objects.get(pk=pk).__dict__
        company = Company.objects.get(pk=job["company_id"])
        job["name"] = company.name
        job["city"] = company.city
        job["company_values"] = company.company_values
        job["domain"] = Profession.objects.get(
            profession=job["proposed_job"]
        ).domain.domain
        if company.photo == "":
            job["photo"] = "https://via.placeholder.com/80"
        else:
            job["photo"] = f"/media/{company.photo}"
        companies_list = json.dumps([job], ensure_ascii=False, default=str)
        return HttpResponse(companies_list, content_type="application/json")

    elif user_type == "student":
        student = Student.objects.get(pk=pk)
        student = student.get_card_infos()
        student = json.dumps([student], ensure_ascii=False, default=str)
        return HttpResponse(student, content_type="application/json")


def send_template_mail(request: HttpRequestWithJob, to_email, template, mail_subject):
    message = render_to_string(
        template,
        {
            "domain": get_current_site(request).domain,
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    email.send()
