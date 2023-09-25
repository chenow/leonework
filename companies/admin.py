from django import forms
from django.contrib import admin

from .models import Company, Job


class CompanyAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyAdminForm, self).__init__(*args, **kwargs)

        self.fields["company_values"].widget = forms.Textarea(attrs={"rows": 2})
        self.fields["overall_atmospheres"].widget = forms.Textarea(attrs={"rows": 2})


class JobAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobAdminForm, self).__init__(*args, **kwargs)

        self.fields["job_description"].widget = forms.Textarea(attrs={"rows": 5})
        self.fields["spoken_languages"].widget = forms.Textarea(attrs={"rows": 3})
        self.fields["qualities"].widget = forms.Textarea(attrs={"rows": 3})


class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAdminForm


class JobAdmin(admin.ModelAdmin):
    list_filter = ("contract_type", "proposed_job", "job_location", "minimal_degree")
    form = JobAdminForm


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
