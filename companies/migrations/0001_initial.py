# Generated by Django 4.2.2 on 2023-06-25 17:34

import companies.validators
import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import students.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("welcome_pages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=100, null=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=12, null=True, region="FR"
                    ),
                ),
                ("adress", models.CharField(max_length=300, null=True)),
                ("city", models.CharField(max_length=100, null=True)),
                ("stripe_id", models.CharField(max_length=200, null=True)),
                ("postal_code", models.IntegerField(null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default="",
                        null=True,
                        upload_to="companies/",
                        validators=[students.validators.validate_file_size],
                    ),
                ),
                (
                    "overall_atmospheres",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("Sérieuse", "Sérieuse"),
                                ("Décontractée", "Décontractée"),
                                ("Coopérative", "Coopérative"),
                                ("Valorisante", "Valorisante"),
                                ("Conviviale", "Conviviale"),
                            ],
                            max_length=20,
                            null=True,
                        ),
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "company_size",
                    models.CharField(
                        choices=[
                            ("petite", "Petite"),
                            ("moyenne", "Moyenne"),
                            ("grande", "Grande"),
                            ("familiale", "Familiale"),
                            ("start-up", "Start-up"),
                        ],
                        max_length=80,
                        null=True,
                    ),
                ),
                ("principal_activity", models.CharField(max_length=100, null=True)),
                (
                    "company_values",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100, null=True),
                        default=list,
                        null=True,
                        size=5,
                    ),
                ),
            ],
            options={
                "verbose_name": "Entreprise",
                "verbose_name_plural": "Entreprises",
                "ordering": ["name", "user__email", "user__date_joined"],
            },
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "contract_type",
                    models.CharField(
                        choices=[
                            ("alternance", "Alternance ou Apprentissage"),
                            ("stage", "Stage"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("minimal_degree", models.CharField(max_length=200, null=True)),
                ("date_publication", models.DateField(auto_now_add=True)),
                ("job_description", models.CharField(max_length=2000, null=True)),
                (
                    "proposed_job",
                    models.CharField(
                        max_length=150,
                        null=True,
                        validators=[companies.validators.check_poste],
                    ),
                ),
                (
                    "teleworking",
                    models.CharField(
                        choices=[
                            ("True", "Oui"),
                            ("False", "Non"),
                            ("None", "A définir"),
                        ],
                        max_length=5,
                        null=True,
                    ),
                ),
                (
                    "hiring",
                    models.CharField(
                        choices=[
                            ("oui", "Oui"),
                            ("non", "Non"),
                            ("pourquoi_pas", "Pourquoi pas"),
                        ],
                        max_length=80,
                        null=True,
                    ),
                ),
                (
                    "beginning_date",
                    models.DateField(default=datetime.date.today, null=True),
                ),
                (
                    "ending_date",
                    models.DateField(default=datetime.date.today, null=True),
                ),
                (
                    "work_weekend",
                    models.CharField(
                        choices=[
                            ("False", "Non"),
                            ("samedi", "Samedi"),
                            ("dimanche", "Dimanche"),
                            ("les_deux", "Les deux"),
                        ],
                        max_length=80,
                        null=True,
                    ),
                ),
                (
                    "spoken_languages",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.CharField(max_length=100, null=True),
                            null=True,
                            size=2,
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "qualities",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100, null=True),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "autonomy",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("faible", "Faible"),
                                ("moyen", "Moyen"),
                                ("important", "Important"),
                            ],
                            max_length=80,
                            null=True,
                        ),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="companies.company",
                    ),
                ),
                (
                    "job_location",
                    models.CharField(
                        max_length=200,
                        null=True,
                        validators=[companies.validators.check_city],
                    ),
                ),
            ],
            options={
                "verbose_name": "Annonce",
                "verbose_name_plural": "Annonces du site (Job)",
                "ordering": ["-date_publication"],
            },
        ),
    ]
