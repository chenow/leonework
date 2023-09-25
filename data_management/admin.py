from django.contrib import admin

from .models import (
    City,
    CompanyValue,
    Degree,
    Domain,
    Language,
    Profession,
    Quality,
)


class CityAdmin(admin.ModelAdmin):
    search_fields = ["city"]

    class Meta:
        model = City


class CompanyValueAdmin(admin.ModelAdmin):
    search_fields = ["value"]

    class Meta:
        model = CompanyValue


class DegreeAdmin(admin.ModelAdmin):
    search_fields = ["subject", "level"]

    class Meta:
        model = Degree


class DomainAdmin(admin.ModelAdmin):
    search_fields = ["domain"]

    class Meta:
        model = Domain


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ["language"]

    class Meta:
        model = Language


class ProfessionAdmin(admin.ModelAdmin):
    search_fields = ["profession"]

    class Meta:
        model = Profession


class QualityAdmin(admin.ModelAdmin):
    search_fields = ["quality"]

    class Meta:
        model = Quality


admin.site.register(City, CityAdmin)
admin.site.register(CompanyValue, CompanyValueAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Quality, QualityAdmin)
