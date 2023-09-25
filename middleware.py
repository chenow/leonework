from typing import Optional
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import logout
from django.shortcuts import redirect

from companies.models import Job
from welcome_pages.models import User


class HttpRequestWithJob(HttpRequest):
    user: User
    job: Optional[Job]


class JobSelectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequestWithJob) -> HttpResponse:
        if not request.user.is_authenticated:
            return self.get_response(request)
        if not request.user.is_company():
            return self.get_response(request)

        assert request.user.company is not None
        job_pk = request.session.get("job", None)

        # check if the job item is from the company
        if (
            job_pk in request.user.company.job_set.values_list("id", flat=True)
            and job_pk is not None
        ):
            request.job = Job.objects.get(pk=job_pk)

        # if not, check if the company has a job
        elif request.user.company.job_set.all():
            request.job = request.user.company.job_set.all()[0]

        # else, something is wrong, logout the user
        else:
            logout(request)
            return redirect("welcome_pages:login")

        return self.get_response(request)

    def process_view(
        # pylint: disable=unused-argument
        self,
        request: HttpRequestWithJob,
        view_func,
        view_args,
        view_kargs: dict,
    ) -> Optional[HttpResponse]:
        job_pk = view_kargs.get("job_pk", None)
        # only true for path "/companies/search/<int:job_pk>/
        # and /companies/researches/<int:job_pk>/"
        if job_pk and request.user.is_authenticated and request.user.is_company():
            job = Job.objects.get(pk=job_pk)
            if job not in request.user.company.job_set.all():
                return HttpResponse(status=403)

            request.session["job"] = job_pk
            request.job = Job.objects.get(pk=job_pk)
        return None
