# Generated by Django 4.2.2 on 2023-07-12 20:33

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0002_alter_student_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region="FR"
            ),
        ),
    ]
