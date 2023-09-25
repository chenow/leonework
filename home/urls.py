from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("index", views.index, name="index"),
    path("faq", views.faq, name="faq"),
    path("support", views.support, name="support"),
    path("change_search", views.change_search, name="change_search"),
    path("likes", views.likes, name="likes"),
    path("matches", views.matches, name="matches"),
    path("messages", views.message, name="messages"),
    path("identity", views.identity, name="identity"),
]
