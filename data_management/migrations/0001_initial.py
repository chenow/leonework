# Generated by Django 4.2.2 on 2023-06-25 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
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
                ("city", models.CharField(max_length=200)),
                ("department", models.CharField(max_length=200)),
                ("region", models.CharField(max_length=200)),
            ],
            options={
                "verbose_name": "Ville",
                "verbose_name_plural": "Villes possibles",
                "ordering": ["city"],
            },
        ),
        migrations.CreateModel(
            name="CompanyValue",
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
                ("value", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Valeur",
                "verbose_name_plural": "Valeurs des entreprises possibles",
                "ordering": ["value"],
            },
        ),
        migrations.CreateModel(
            name="Degree",
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
                    "level",
                    models.CharField(
                        choices=[
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
                            ("DSCG", "DSCG"),
                            ("Licence", "Licence"),
                            ("Licence Professionnelle", "Licence Professionnelle"),
                            ("MBA", "MBA"),
                            ("MS", "MS"),
                            ("Master", "Master"),
                            ("Titre ingénieur", "Titre ingénieur"),
                        ],
                        max_length=350,
                    ),
                ),
                ("subject", models.CharField(max_length=350)),
            ],
            options={
                "verbose_name": "Diplôme",
                "verbose_name_plural": "Diplômes possibles",
                "ordering": ["level"],
            },
        ),
        migrations.CreateModel(
            name="Domain",
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
                ("domain", models.CharField(max_length=300)),
            ],
            options={
                "verbose_name": "Domaine",
                "verbose_name_plural": "Domaines des métiers",
                "ordering": ["domain"],
            },
        ),
        migrations.CreateModel(
            name="Language",
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
                ("language", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Langue",
                "verbose_name_plural": "Langues parlées possibles",
                "ordering": ["language"],
            },
        ),
        migrations.CreateModel(
            name="Quality",
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
                ("quality", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Qualité",
                "verbose_name_plural": "Qualités des étudiants possibles",
                "ordering": ["quality"],
            },
        ),
        migrations.CreateModel(
            name="Profession",
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
                ("profession", models.CharField(max_length=300)),
                (
                    "domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="data_management.domain",
                    ),
                ),
            ],
            options={
                "verbose_name": "Métier",
                "verbose_name_plural": "Liste des métiers",
                "ordering": ["profession"],
            },
        ),
    ]