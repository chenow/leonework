from datetime import datetime, timedelta

from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import QueryDict


from data_management.models import Profession, City
from students.models import Student

from companies.models import Job


def get_matching_students(job: Job, params: QueryDict) -> QuerySet[Student]:
    if params.get("matchingOndomaine") == "false":
        students = Student.objects.filter(demanded_jobs__overlap=[job.proposed_job])
    else:
        domain = Profession.objects.get(profession=job.proposed_job).domain
        metiers_recherches = list(
            Profession.objects.filter(domain=domain).values_list(
                "profession", flat=True
            )
        )
        students = Student.objects.filter(
            Q(demanded_domains__overlap=[domain])
            | Q(demanded_jobs__overlap=metiers_recherches)
        )

    students = students.filter(
        contract_type=job.contract_type,
        qualities__overlap=job.qualities,
        overall_atmospheres__overlap=job.company.overall_atmospheres,
        company_values__overlap=job.company.company_values,
        company_sizes__overlap=[job.company.company_size],
    )

    beginning_date = params.get("DateDebutMission")
    if beginning_date:
        beginning_date = datetime.strptime(beginning_date, "%d/%m/%Y")
    else:
        beginning_date = datetime.now()

    students = students.filter(
        beginning_date__range=[
            beginning_date - timedelta(days=31 * 3),
            beginning_date + timedelta(days=31 * 3),
        ],
    )
    if params.get("matchingOnDepartement") == "false":
        students = students.filter(company_locations__overlap=[job.job_location])
    else:
        region = City.objects.get(city=job.job_location).region
        cities = City.objects.filter(region=region).values_list("city", flat=True)
        students = students.filter(company_locations__overlap=cities)

    autonomy = params.get("matchingOnEncadrement", "").split(",")
    students = students.filter(autonomy__overlap=autonomy)
    if params.get("matchingOnWeekend") == "samedi":
        students = students.filter(work_weekend__in=["samedi", "les_deux"])
    elif params.get("matchingOnWeekend") == "dimanche":
        students = students.filter(work_weekend__in=["dimanche", "les_deux"])
    elif params.get("matchingOnWeekend") == "les_deux":
        students = students.filter(work_weekend__in=["dimanche", "samedi", "les_deux"])
    elif params.get("matchingOnWeekend") == "False":
        pass
    if params.get("matchingOnteleworking") == "None":
        pass
    else:
        students = students.filter(
            teleworking__in=["None", params.get("matchingOnteleworking")]
        )
    students = [
        student
        for student in students
        if student.pk
        not in job.like_set.filter(company_liked=True).values_list("student", flat=True)
    ]

    return students


def filter_by_degree_level(students: QuerySet[Student], job: Job) -> QuerySet[Student]:
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
            "Licence - 1ère année",
            "Licence - 2ème année",
            "Licence - 3ème année",
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
            "Master - 1ère année",
            "Master - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
        ],
        "niveau 2": [
            "Licence Professionnelle - 2ème année",
            "Licence Professionnelle - 3ème année",
            "Licence - 2ème année",
            "Licence - 3ème année",
            "BACHELOR - 2ème année",
            "BACHELOR - 3ème année",
            "BUT - 2ème année",
            "BUT - 3ème année",
            "Titre ingénieur - 2ème année",
            "Titre ingénieur - 3ème année",
            "MBA - 1ère année",
            "MBA - 2ème année",
            "Master - 1ère année",
            "Master - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
        ],
        "niveau 3": [
            "Licence Professionnelle - 3ème année",
            "Licence - 3ème année",
            "BACHELOR - 3ème année",
            "BUT - 3ème année",
            "Titre ingénieur - 3ème année",
            "MBA - 1ère année",
            "MBA - 2ème année",
            "Master - 1ère année",
            "Master - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
        ],
        "niveau 4": [
            "MBA - 1ère année",
            "MBA - 2ème année",
            "Master - 1ère année",
            "Master - 2ème année",
            "MS - 1ère année",
            "MS - 2ème année",
            "Titre ingénieur - 3ème année",
        ],
        "niveau 5 :": [
            "Titre ingénieur - 3ème année",
            "MBA - 2ème année",
            "Master - 2ème année",
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
            "DSCG - 1ère année",
            "DSCG - 2ème année",
        ],
        "niveau 2": [
            "DCG - 2ème année",
            "DCG - 3ème année",
            "DSCG - 1ère année",
            "DSCG - 2ème année",
        ],
        "niveau 3": [
            "DCG - 3ème année",
            "DSCG - 1ère année",
            "DSCG - 2ème année",
        ],
        "niveau 4": [
            "DSCG - 1ère année",
            "DSCG - 2ème année",
        ],
        "niveau 5": [
            "DSCG - 2ème année",
        ],
    }
    students_filtered = []
    degrees_searched = []
    for _, levels in order.items():
        for _, degrees in levels.items():
            if job.minimal_degree in degrees:
                degrees_searched = degrees

    for student in students:
        for degree in degrees_searched:
            degree, year = degree.split(" - ")
            if (
                student not in students_filtered
                and degree in student.ongoing_degree
                and year in student.ongoing_year
            ):
                students_filtered.append(student)
    return students_filtered
