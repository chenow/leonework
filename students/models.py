from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date
from django.db import models
from django.contrib.postgres.fields import ArrayField

from phonenumber_field.modelfields import PhoneNumberField

from welcome_pages.models import User

from .validators import validate_file_size

if TYPE_CHECKING:
    from matching.models import Chats, Like


class Student(models.Model):
    like_set: models.QuerySet[Like]
    chats_set: models.QuerySet[Chats]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    # Mon identité
    first_name = models.CharField(
        max_length=100,
        null=True,
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
    )
    phone_number = PhoneNumberField(
        null=True,
        region="FR",
    )  # type: ignore
    birthdate = models.DateField(
        null=True,
    )
    photo = models.ImageField(
        upload_to="students/",
        default="",
        null=True,
        blank=True,
        validators=[validate_file_size],
    )

    # Mon parcours
    ongoing_degree = models.CharField(
        max_length=350,
        null=True,
        blank=True,
    )
    school = models.CharField(max_length=100, null=True)

    ONGOING_YEAR_CHOICES = [
        ["1ère année", "année 1"],
        ["2ème année", "année 2"],
        ["3ème année", "année 3"],
    ]
    ongoing_year = models.CharField(
        max_length=50,
        null=True,
        choices=ONGOING_YEAR_CHOICES,  # type: ignore
    )
    last_degree = models.CharField(max_length=350, null=True)
    experiences = ArrayField(
        ArrayField(models.CharField(max_length=100, null=True), size=3, null=True),
        default=list,
        null=True,
        blank=True,
    )

    # Atouts
    spoken_languages = ArrayField(
        ArrayField(models.CharField(max_length=100, null=True), size=2, null=True),
        default=list,
        blank=True,
        null=True,
    )

    qualities = ArrayField(
        models.CharField(max_length=100, null=True),
        size=5,
        null=True,
    )
    future_vision = models.CharField(max_length=300, null=True)

    # La mission que je recherche
    CONTRACTS = [
        ("alternance", "Alternance ou Apprentissage"),
        ("stage", "Stage"),
    ]
    contract_type = models.CharField(
        choices=CONTRACTS,
        max_length=100,
        null=True,
    )
    apprenticeship_rate = models.CharField(max_length=100, null=True, blank=True)
    beginning_date = models.DateField(default=date.today, null=True)
    ending_date = models.DateField(default=date.today, null=True)
    demanded_jobs = ArrayField(
        models.CharField(max_length=150, null=True),
        default=list,
        blank=True,
        null=True,
    )
    demanded_domains = ArrayField(
        models.CharField(max_length=150, null=True),
        default=list,
        blank=True,
        null=True,
    )
    TELEWORKING = [
        ("True", "Oui"),
        ("False", "Non"),
        ("None", "A définir"),
    ]
    teleworking = models.CharField(choices=TELEWORKING, max_length=5, null=True)
    WORK_WEEKEND = [
        ("False", "Non"),
        ("samedi", "Samedi"),
        ("dimanche", "Dimanche"),
        ("les_deux", "Les deux"),
    ]
    work_weekend = models.CharField(choices=WORK_WEEKEND, max_length=10, null=True)

    # Mon entreprise idéale
    COMPANY_SIZES = [
        ("petite", "Petite"),
        ("moyenne", "Moyenne"),
        ("grande", "Grande"),
        ("familiale", "Familiale"),
        ("start-up", "Start-up"),
    ]

    OVERALL_ATMOSPHERES = [
        ("Sérieuse", "Sérieuse"),
        ("Décontractée", "Décontractée"),
        ("Coopérative", "Coopérative"),
        ("Valorisante", "Valorisante"),
        ("Conviviale", "Conviviale"),
    ]

    overall_atmospheres = ArrayField(
        models.CharField(choices=OVERALL_ATMOSPHERES, max_length=80, null=True),
        default=list,
        null=True,
    )

    company_sizes = ArrayField(
        models.CharField(choices=COMPANY_SIZES, max_length=80, null=True),
        default=list,
        null=True,
    )
    company_locations = ArrayField(
        models.CharField(max_length=200, null=True),
        default=list,
        null=True,
    )
    company_values = ArrayField(
        models.CharField(max_length=100, null=True),
        default=list,
        size=5,
        null=True,
    )
    AUTONOMY = [
        ("faible", "Faible"),
        ("moyen", "Moyen"),
        ("important", "Important"),
    ]

    autonomy = ArrayField(
        models.CharField(choices=AUTONOMY, max_length=80, null=True),
        default=list,
        null=True,
    )

    HIRING = [
        ("oui", "Oui"),
        ("non", "Non"),
        ("pourquoi_pas", "Pourquoi pas"),
    ]
    hiring = models.CharField(choices=HIRING, max_length=50, null=True)

    def __str__(self):
        if self.first_name is None or self.last_name is None:
            return self.user.email
        return f"{self.first_name} {self.last_name} - {self.user.email}"

    def save(self, *args, **kwargs):
        if self.first_name is not None:
            self.first_name = self.first_name.capitalize()
        if self.last_name is not None:
            self.last_name = self.last_name.capitalize()
        super(Student, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-user__date_joined"]
        verbose_name_plural = "Étudiants"
        verbose_name = "Étudiant"

    def get_card_infos(self) -> dict:
        infos = self.__dict__
        infos["beginning_date"] = infos["beginning_date"].strftime("%d %B %Y")
        infos["ending_date"] = infos["ending_date"].strftime("%d %B %Y")
        infos["contract_type"] = infos["contract_type"].capitalize()

        infos["photo"] = (
            f"/media/{self.photo}"
            if (self.photo and self.photo != "")
            else "https://via.placeholder.com/80"
        )
        return infos
