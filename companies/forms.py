from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from .models import Company, Job

degree_choices = [
    ["CAP - 1ère année", "CAP - 1ère année"],
    ["CAP - 2ème année", "CAP - 2ème année"],
    ["BP - 1ère année", "BP - 1ère année"],
    ["BP - 2ème année", "BP - 2ème année"],
    ["BAC PRO - 1ère année", "BAC PRO - 1ère année"],
    ["BAC PRO - 2ème année", "BAC PRO - 2ème année"],
    ["BTS - 1ère année", "BTS - 1ère année"],
    ["BTS - 2ème année", "BTS - 2ème année"],
    ["DEUST - 1ère année", "DEUST - 1ère année"],
    ["DEUST - 2ème année", "DEUST - 2ème année"],
    ["Licence Professionnelle - 1ère année", "Licence Professionnelle - 1ère année"],
    ["Licence Professionnelle - 2ème année", "Licence Professionnelle - 2ème année"],
    ["Licence Professionnelle - 3ème année", "Licence Professionnelle - 3ème année"],
    ["Licence - 1ère année", "Licence - 1ère année"],
    ["Licence - 2ème année", "Licence - 2ème année"],
    ["Licence - 3ème année", "Licence - 3ème année"],
    ["BACHELOR - 1ère année", "BACHELOR - 1ère année"],
    ["BACHELOR - 2ème année", "BACHELOR - 2ème année"],
    ["BACHELOR - 3ème année", "BACHELOR - 3ème année"],
    ["BUT - 1ère année", "BUT - 1ère année"],
    ["BUT - 2ème année", "BUT - 2ème année"],
    ["BUT - 3ème année", "BUT - 3ème année"],
    ["DMA - 1ère année", "DMA - 1ère année"],
    ["DMA - 2ème année", "DMA - 2ème année"],
    ["DMA - 3ème année", "DMA - 3ème année"],
    ["Master - 1ère année", "Master - 1ère année"],
    ["Master - 2ème année", "Master - 2ème année"],
    ["MBA - 1ère année", "MBA - 1ère année"],
    ["MBA - 2ème année", "MBA - 2ème année"],
    ["MS - 1ère année", "MS - 1ère année"],
    ["MS - 2ème année", "MS - 2ème année"],
    ["DCG - 1ère année", "DCG - 1ère année"],
    ["DCG - 2ème année", "DCG - 2ème année"],
    ["DCG - 3ème année", "DCG - 3ème année"],
    ["DSCG - 1ère année", "dscg - 1ère année"],
    ["DSCG - 2ème année", "dscg - 2ème année"],
    ["Titre ingénieur - 1ère année", "Titre ingénieur - 1ère année"],
    ["Titre ingénieur - 2ème année", "Titre ingénieur - 2ème année"],
    ["Titre ingénieur - 3ème année", "Titre ingénieur - 3ème année"],
]


class IdentityForm(forms.ModelForm):
    postal_code = forms.CharField()
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "+07..."})
    )

    class Meta:
        model = Company
        fields = ["name", "phone_number", "adress", "postal_code", "photo", "city"]

    def __init__(self, *args, **kwargs):
        translation = {
            "name": "Nom de l'entreprise",
            "adress": "Adresse",
            "postal_code": "Code postal",
            "city": "Ville",
            "phone_number": "Téléphone",
            "photo": "Photo de profil",
        }
        super(IdentityForm, self).__init__(*args, **kwargs)
        for field, label in translation.items():
            self.fields[field].label = label
            self.fields[field].widget.attrs["placeholder"] = label


class EntrepriseForm(forms.ModelForm):
    company_size = forms.ChoiceField(
        widget=forms.RadioSelect, required=True, choices=Company.COMPANY_SIZE
    )

    overall_atmospheres = forms.MultipleChoiceField(
        choices=Company.OVERALL_ATMOSPHERES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Company
        fields = [
            "company_size",
            "company_values",
            "overall_atmospheres",
            "principal_activity",
        ]

    def __init__(self, *args, **kwargs):
        super(EntrepriseForm, self).__init__(*args, **kwargs)
        self.fields["company_size"].label = "Sa taille"
        self.fields["company_values"].label = "Nos valeurs"
        self.fields["overall_atmospheres"].label = "Ambiance générale"
        self.fields["principal_activity"].label = "Notre activité principale"


class MissionForm(forms.ModelForm):
    contract_type = forms.ChoiceField(
        choices=Job.CONTRACTS,
        required=True,
    )
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}), required=True
    )
    minimal_degree = forms.ChoiceField(
        choices=degree_choices,  # type: ignore
        required=True,
    )

    teleworking = forms.ChoiceField(
        choices=Job.TELEWORKING,
        widget=forms.RadioSelect,
        required=True,
    )
    work_weekend = forms.ChoiceField(
        choices=Job.WORK_WEEKEND,
        widget=forms.RadioSelect,
        required=True,
    )

    hiring = forms.ChoiceField(
        choices=Job.HIRING,
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Job
        fields = [
            "contract_type",
            "minimal_degree",
            "beginning_date",
            "ending_date",
            "proposed_job",
            "job_description",
            "teleworking",
            "hiring",
            "work_weekend",
            "job_location",
        ]

    def __init__(self, *args, **kwargs):
        super(MissionForm, self).__init__(*args, **kwargs)
        self.fields["beginning_date"].label = "Date de début"
        self.fields["contract_type"].label = "Type de contrat"
        self.fields["ending_date"].label = "Date de fin"
        self.fields["teleworking"].label = "Proposons nous du télétravail ?"
        self.fields[
            "hiring"
        ].label = (
            "Si le candidat me convient, souhaitons nous l'embaucher ( en CDI, CDD) ?"
        )
        self.fields["job_description"].label = "Description de la mission"
        self.fields["work_weekend"].label = "Travail le weekend"
        self.fields["job_location"].label = "Lieu de la mission"
        self.fields["proposed_job"].label = "Poste proposé"
        self.fields["minimal_degree"].label = "Niveau du diplôme en préparation"


class CandidatForm(forms.ModelForm):
    autonomy = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=Job.AUTONOMY, required=True
    )
    spoken_languages = SimpleArrayField(
        SimpleArrayField(forms.CharField()), required=False, delimiter="|"
    )

    class Meta:
        model = Job
        fields = ["spoken_languages", "autonomy", "qualities"]

    def __init__(self, *args, **kwargs):
        super(CandidatForm, self).__init__(*args, **kwargs)
        self.fields["autonomy"].label = "Quel encadrement pouvons nous lui apporter ?"


class JobForm(forms.ModelForm):
    contract_type = forms.ChoiceField(
        choices=Job.CONTRACTS,
        required=True,
    )
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}), required=True
    )
    minimal_degree = forms.ChoiceField(
        choices=degree_choices,  # type: ignore
        required=True,
    )

    teleworking = forms.ChoiceField(
        choices=Job.TELEWORKING,
        widget=forms.RadioSelect,
        required=True,
    )
    work_weekend = forms.ChoiceField(
        choices=Job.WORK_WEEKEND,
        widget=forms.RadioSelect,
        required=True,
    )

    hiring = forms.ChoiceField(
        choices=Job.HIRING,
        widget=forms.RadioSelect,
        required=True,
    )

    autonomy = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=Job.AUTONOMY, required=True
    )
    spoken_languages = SimpleArrayField(
        SimpleArrayField(forms.CharField()), required=False, delimiter="|"
    )

    class Meta:
        model = Job
        fields = [
            "spoken_languages",
            "autonomy",
            "qualities",
            "contract_type",
            "minimal_degree",
            "beginning_date",
            "ending_date",
            "job_description",
            "teleworking",
            "hiring",
            "work_weekend",
            "proposed_job",
            "job_location",
        ]

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields["autonomy"].label = "Quel encadrement pouvons nous lui apporter ?"
        self.fields["beginning_date"].label = "Date de début"
        self.fields["ending_date"].label = "Date de fin"
        self.fields["teleworking"].label = "Proposons nous du télétravail ?"
        self.fields[
            "hiring"
        ].label = (
            "Si le candidat me convient, souhaitons nous l'embaucher ( en CDI, CDD) ?"
        )
        self.fields["job_description"].label = "Description de la mission"
        self.fields["work_weekend"].label = "Travail le weekend"
        self.fields["job_location"].label = "Lieu de la mission"
        self.fields["minimal_degree"].label = "Niveau du diplôme en préparation"
        self.fields["proposed_job"].label = "Intitulé du poste"


class EngagementForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["engagement"]
