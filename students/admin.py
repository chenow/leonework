from django.contrib import admin
from django import forms
from django.db.models import Q

from data_management.models import Domain, Profession

from .models import Student


class StudentAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentAdminForm, self).__init__(*args, **kwargs)

        self.fields["spoken_languages"].widget = forms.Textarea(attrs={"rows": 2})
        self.fields["future_vision"].widget = forms.Textarea(attrs={"rows": 5})
        self.fields["spoken_languages"].widget = forms.Textarea(attrs={"rows": 2})
        self.fields["experiences"].widget = forms.Textarea(attrs={"rows": 4})
        self.fields["demanded_domains"].widget = forms.Textarea(attrs={"rows": 3})
        self.fields["company_values"].widget = forms.Textarea(attrs={"rows": 3})
        self.fields["qualities"].widget = forms.Textarea(attrs={"rows": 3})


class arrayLocalisation_entreprise(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField."""

    title = "Ville"
    parameter_name = "company_locations"

    def lookups(self, request, model_admin):
        # Very similar to our code above, but this method must return a
        # list of tuples: (lookup_value, human-readable value). These
        # appear in the admin's right sidebar

        keywords = Student.objects.exclude(company_locations=None).values_list(
            "company_locations", flat=True
        )
        keywords = [(kw, kw) for sublist in keywords for kw in sublist if kw]
        keywords = sorted(set(keywords))
        return keywords

    def queryset(self, request, queryset):
        # when a user clicks on a filter, this method gets called. The
        # provided queryset with be a queryset of Items, so we need to
        # filter that based on the clicked keyword.

        lookup_value = self.value()  # The clicked keyword. It can be None!
        if lookup_value:
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(company_locations__contains=[lookup_value])
        return queryset


class arraydemanded_jobs(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField."""

    title = "Poste recherché"
    parameter_name = "demanded_jobs"

    def lookups(self, request, model_admin):
        # Very similar to our code above, but this method must return a
        # list of tuples: (lookup_value, human-readable value). These
        # appear in the admin's right sidebar
        keywords = Student.objects.exclude(demanded_jobs=None).values_list(
            "demanded_jobs", flat=True
        )
        keywords = [(kw, kw) for sublist in keywords for kw in sublist if kw]
        keywords = sorted(set(keywords))
        return keywords

    def queryset(self, request, queryset):
        # when a user clicks on a filter, this method gets called. The
        # provided queryset with be a queryset of Items, so we need to
        # filter that based on the clicked keyword.

        lookup_value = self.value()  # The clicked keyword. It can be None!
        if lookup_value:
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(demanded_jobs__contains=[lookup_value])
        return queryset


class arrayDomaines_recherches(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField."""

    title = "Domaine recherché"
    parameter_name = "demanded_domains"

    def lookups(self, request, model_admin):
        # Very similar to our code above, but this method must return a
        # list of tuples: (lookup_value, human-readable value). These
        # appear in the admin's right sidebar

        keywords = Student.objects.exclude(demanded_jobs=None).values_list(
            "demanded_domains", flat=True
        )
        keywords = [(kw, kw) for sublist in keywords for kw in sublist if kw]
        keywords = sorted(set(keywords))
        return keywords

    def queryset(self, request, queryset):
        # when a user clicks on a filter, this method gets called. The
        # provided queryset with be a queryset of Items, so we need to
        # filter that based on the clicked keyword.

        lookup_value = self.value()  # The clicked keyword. It can be None!
        if lookup_value:
            domain = Domain.objects.get(domain=lookup_value)
            professions = Profession.objects.filter(domain=domain).values_list(
                "profession", flat=True
            )
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(
                Q(demanded_domains__overlap=[lookup_value])
                | Q(demanded_jobs__overlap=list(professions)),
            )
        return queryset


class StudentAdmin(admin.ModelAdmin):
    search_fields = ["last_name", "user__email"]
    list_filter = (
        arrayLocalisation_entreprise,
        arraydemanded_jobs,
        arrayDomaines_recherches,
        "contract_type",
    )
    form = StudentAdminForm
    list_display = (
        "last_name",
        "first_name",
        "phone_number",
    )


admin.site.register(Student, StudentAdmin)
