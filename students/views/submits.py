import json

from django.http import HttpResponse
from django.shortcuts import render

from middleware import HttpRequestWithJob


def select_experiences(request: HttpRequestWithJob):
    assert request.user.student is not None
    return render(
        request,
        "students/components/experiences.html",
        {"experiences": request.user.student.experiences},
    )


def add_experience(request: HttpRequestWithJob):
    assert request.user.student is not None
    experience = [
        request.GET.get("type"),
        request.GET.get("ent"),
        request.GET.get("duree"),
    ]
    if None in experience:
        return HttpResponse(status=400)
    request.user.student.experiences.append(experience)
    request.user.student.experiences = [experience]
    request.user.student.save()
    return render(
        request,
        "students/components/experiences.html",
        {"experiences": request.user.student.experiences},
    )


def delete_experience(request: HttpRequestWithJob, experience):
    assert request.user.student is not None
    request.user.student.experiences.pop(experience)
    request.user.student.save()
    return render(
        request,
        "students/components/experiences.html",
        {"experiences": request.user.student.experiences},
    )


def langs(request: HttpRequestWithJob):
    assert request.user.student is not None
    langues = json.loads(request.body)
    request.user.student.spoken_languages = langues["langs"]
    request.user.student.save()
    return HttpResponse(status=202)


def get_langs(request: HttpRequestWithJob):
    assert request.user.student is not None
    return render(
        request,
        "students/components/langs.html",
        {"langs": request.user.student.spoken_languages},
    )


def qualities(request: HttpRequestWithJob):
    assert request.user.student is not None
    new_qualities = json.loads(request.body)
    request.user.student.qualities = new_qualities["qualities"]
    request.user.student.save()
    return HttpResponse(status=202)


def get_qualities(request: HttpRequestWithJob):
    assert request.user.student is not None
    return render(
        request,
        "students/components/qualities.html",
        {"qualities": request.user.student.qualities},
    )


def valeurs(request: HttpRequestWithJob):
    assert request.user.student is not None
    new_valeurs = json.loads(request.body)
    request.user.student.company_values = new_valeurs["valeurs"]
    request.user.student.save()
    return HttpResponse(status=202)


def get_valeurs(request: HttpRequestWithJob):
    assert request.user.student is not None
    return render(
        request,
        "students/components/valeurs.html",
        {"valeurs": request.user.student.company_values},
    )


def get_cities(request: HttpRequestWithJob):
    assert request.user.student is not None
    return render(
        request,
        "students/components/cities.html",
        {"cities": request.user.student.company_locations},
    )


def save_cities(request: HttpRequestWithJob):
    assert request.user.student is not None
    cities = json.loads(request.body)
    request.user.student.company_locations = cities["cities"]
    request.user.student.save()
    return HttpResponse(status=202)
