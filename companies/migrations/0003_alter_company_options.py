# Generated by Django 4.2.2 on 2023-06-30 09:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0002_company_engagement"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="company",
            options={
                "ordering": ["-user__date_joined"],
                "verbose_name": "Entreprise",
                "verbose_name_plural": "Entreprises",
            },
        ),
    ]
