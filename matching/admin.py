from django.contrib import admin
from .models import Like, Chats


class LikeAdmin(admin.ModelAdmin):
    list_display = ("job", "student", "company_liked", "student_liked")
    search_fields = ("job__company__name", "student__last_name")


class ChatsAdmin(admin.ModelAdmin):
    list_display = ("chat", "by", "job", "student", "date")
    search_fields = ("job__company__name", "student__last_name")

    class Media:
        css = {"all": ("css/admin.css",)}


admin.site.register(Like, LikeAdmin)
admin.site.register(Chats, ChatsAdmin)
