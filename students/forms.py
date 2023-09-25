from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from data_management.models import Degree


from .models import Student


class IdentityForm(forms.ModelForm):
    template_name = "students/forms/identity.html"
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "+33 7..."})
    )

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "birthdate",
            "photo",
        ]

    def __init__(self, *args, **kwargs):
        super(IdentityForm, self).__init__(*args, **kwargs)
        translation = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "phone_number": "Téléphone",
            "birthdate": "Date de naissance",
            "photo": "Photo de profil",
        }
        for field, label in translation.items():
            self.fields[field].label = label
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = label


class ParcoursForm(forms.ModelForm):
    ongoing_degree = forms.ChoiceField(
        required=True,
        choices=[],
    )
    experiences = SimpleArrayField(
        SimpleArrayField(forms.CharField(), delimiter=","),
        required=False,
        delimiter=";",
    )

    class Meta:
        model = Student
        fields = [
            "ongoing_degree",
            "school",
            "ongoing_year",
            "last_degree",
            "experiences",
        ]

    def __init__(self, *args, **kwargs):
        super(ParcoursForm, self).__init__(*args, **kwargs)
        self.fields["ongoing_degree"].choices = [
            (f"{degree.level} - {degree.subject}", f"{degree.level} - {degree.subject}")
            for degree in Degree.objects.all()
        ]


class AtoutsForm(forms.ModelForm):
    spoken_languages = SimpleArrayField(
        SimpleArrayField(forms.CharField()), required=False, delimiter="|"
    )
    qualities = SimpleArrayField(forms.CharField(max_length=100))

    class Meta:
        model = Student
        fields = ["future_vision", "spoken_languages", "qualities"]


class MissionForm(forms.ModelForm):
    template_name = "students/forms/mission.html"
    demanded_job = SimpleArrayField(forms.CharField(max_length=100), required=False)
    demanded_domains = SimpleArrayField(
        forms.CharField(max_length=150), required=False, delimiter="|"
    )
    work_weekend = forms.ChoiceField(required=True, choices=Student.WORK_WEEKEND)
    teleworking = forms.ChoiceField(required=True, choices=Student.TELEWORKING)

    class Meta:
        model = Student
        fields = [
            "contract_type",
            "apprenticeship_rate",
            "beginning_date",
            "ending_date",
            "demanded_jobs",
            "teleworking",
            "work_weekend",
            "demanded_domains",
        ]


class EntrepriseForm(forms.ModelForm):
    template_name = "students/forms/entreprise.html"

    company_sizes = forms.MultipleChoiceField(choices=Student.COMPANY_SIZES)
    overall_atmospheres = forms.MultipleChoiceField(choices=Student.OVERALL_ATMOSPHERES)
    autonomy = forms.MultipleChoiceField(choices=Student.AUTONOMY, required=True)
    hiring = forms.ChoiceField(choices=Student.HIRING)

    class Meta:
        model = Student
        fields = [
            "company_sizes",
            "overall_atmospheres",
            "autonomy",
            "hiring",
            "company_locations",
            "company_values",
        ]


class changeSearchForms(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "company_sizes",
            "overall_atmospheres",
            "autonomy",
            "hiring",
        ]
