from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING
from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from data_management.models import Profession
from students.validators import validate_file_size

from welcome_pages.models import User

from .validators import check_city, check_poste

if TYPE_CHECKING:
    from matching.models import Like, Chats


class Company(models.Model):
    job_set: models.QuerySet[Job]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=100, null=True)
    phone_number = PhoneNumberField(
        # type: ignore
        region="FR",
        max_length=12,
        null=True,
    )
    adress = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=100, null=True)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.IntegerField(null=True)
    photo = models.ImageField(
        upload_to="companies/",
        validators=[validate_file_size],
        null=True,
        blank=True,
        default="",
    )

    # Entreprise
    OVERALL_ATMOSPHERES = [
        ("Sérieuse", "Sérieuse"),
        ("Décontractée", "Décontractée"),
        ("Coopérative", "Coopérative"),
        ("Valorisante", "Valorisante"),
        ("Conviviale", "Conviviale"),
    ]
    overall_atmospheres = ArrayField(
        models.CharField(choices=OVERALL_ATMOSPHERES, max_length=20, null=True),
        default=list,
        null=True,
    )

    COMPANY_SIZE = [
        ("petite", "Petite"),
        ("moyenne", "Moyenne"),
        ("grande", "Grande"),
        ("familiale", "Familiale"),
        ("start-up", "Start-up"),
    ]

    company_size = models.CharField(max_length=80, null=True, choices=COMPANY_SIZE)

    principal_activity = models.CharField(max_length=100, null=True)
    company_values = ArrayField(
        models.CharField(max_length=100, null=True),
        size=5,
        default=list,
        null=True,
    )

    engagement = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.name}"

    class Meta:
        verbose_name_plural = "Entreprises"
        verbose_name = "Entreprise"
        ordering = ["-user__date_joined"]


class Job(models.Model):
    like_set: models.QuerySet[Like]
    chats_set: models.QuerySet[Chats]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Mission
    CONTRACTS = [
        ("alternance", "Alternance ou Apprentissage"),
        ("stage", "Stage"),
    ]
    contract_type = models.CharField(
        choices=CONTRACTS,
        max_length=100,
        null=True,
    )
    DEGREES = [
        ("BAC PRO", "BAC PRO"),
        ("BACHELOR", "BACHELOR"),
        ("BM", "BM"),
        ("BP", "BP"),
        ("BTS", "BTS"),
        ("BUT", "BUT"),
        ("CAP", "CAP"),
        ("DCG", "DCG"),
        ("DEC", "DEC"),
        ("DEUST", "DEUST"),
        ("DMA", "DMA"),
        ("Licence", "Licence"),
        ("Licence Professionnelle", "Licence Professionnelle"),
        ("Master", "Master"),
        ("MBA", "MBA"),
        ("MS", "MS"),
        ("DSCG", "DSCG"),
        ("Titre ingénieur", "Titre ingénieur"),
    ]
    date_publication = models.DateField(auto_now_add=True)

    minimal_degree = models.CharField(
        max_length=200,
        null=True,
    )
    job_description = models.CharField(
        max_length=2000,
        null=True,
    )
    proposed_job = models.CharField(max_length=150, null=True, validators=[check_poste])
    TELEWORKING = [
        ("True", "Oui"),
        ("False", "Non"),
        ("None", "A définir"),
    ]
    teleworking = models.CharField(
        choices=TELEWORKING,
        max_length=5,
        null=True,
    )
    HIRING = [
        ("oui", "Oui"),
        ("non", "Non"),
        ("pourquoi_pas", "Pourquoi pas"),
    ]
    hiring = models.CharField(choices=HIRING, max_length=80, null=True)
    beginning_date = models.DateField(null=True, default=date.today)
    ending_date = models.DateField(null=True, default=date.today)
    WORK_WEEKEND = [
        ("False", "Non"),
        ("samedi", "Samedi"),
        ("dimanche", "Dimanche"),
        ("les_deux", "Les deux"),
    ]
    work_weekend = models.CharField(choices=WORK_WEEKEND, max_length=80, null=True)

    # Candidat
    spoken_languages = ArrayField(
        ArrayField(
            models.CharField(max_length=100, null=True),
            size=2,
            null=True,
        ),
        null=True,
        blank=True,
    )
    qualities = ArrayField(
        models.CharField(max_length=100, null=True),
        null=True,
    )

    AUTONOMY = [
        ("faible", "Faible"),
        ("moyen", "Moyen"),
        ("important", "Important"),
    ]
    autonomy = ArrayField(
        models.CharField(
            choices=AUTONOMY,
            max_length=80,
            null=True,
        ),
        null=True,
    )

    job_location = models.CharField(max_length=200, null=True, validators=[check_city])

    def __str__(self):
        return f"{self.company.name} - {self.proposed_job}"

    class Meta:
        ordering = ["-date_publication"]
        verbose_name_plural = "Annonces du site (Job)"
        verbose_name = "Annonce"

    def get_job_infos(self) -> dict:
        job_dict = self.__dict__
        job_dict["name"] = self.company.name
        job_dict["principal_activity"] = self.company.principal_activity
        job_dict["company_values"] = self.company.company_values
        job_dict["overall_atmospheres"] = self.company.overall_atmospheres
        job_dict["company_size"] = self.company.company_size
        job_dict["beginning_date"] = job_dict["beginning_date"].strftime("%d %B %Y")
        job_dict["ending_date"] = job_dict["ending_date"].strftime("%d %B %Y")
        job_dict["principal_acitvity"] = self.company.principal_activity
        job_dict["domain"] = Profession.objects.get(
            profession=job_dict["proposed_job"]
        ).domain
        if self.company.photo == "":
            job_dict["photo"] = "https://via.placeholder.com/80"
        else:
            job_dict["photo"] = f"/media/{self.company.photo}"
        return job_dict
