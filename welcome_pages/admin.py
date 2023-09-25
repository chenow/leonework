from django.contrib import admin
from django.contrib.auth.models import Group

from welcome_pages.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "date_joined",
        "last_login",
        "finished_inscription",
    )
    search_fields = ["email"]
    date_hierarchy = "date_joined"
    exclude = (
        "password",
        "groups",
        "user_permissions",
        "is_staff",
        "first_name",
        "last_name",
    )


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
