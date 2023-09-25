from django.urls import path


from home.views import index
from . import views


app_name = "welcome_pages"

url_accueil = [
    path("", index, name="index"),
    path("presentation", views.presentation, name="presentation"),
    path("register/", views.register, name="register"),
    path("login/", views.own_login, name="login"),
    path("logout/", views.own_logout, name="logout"),
    path("mentions_legales/", views.mentions_legales, name="mentions_legales"),
    path("cookies/", views.cookies, name="cookies"),
    path("confidentialite/", views.confidentialite, name="confidentialite"),
    path("cgv/", views.cgv, name="cgv"),
    path("cgu/", views.cgu, name="cgu"),
    path(
        "beginning_inscription/",
        views.beginning_inscription,
        name="beginning_inscription",
    ),
    path("waiting_mail_check/", views.waiting_mail_check, name="waiting_mail_check"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("email", views.mailAcceuil, name="mail"),
]

url_reset_password = []

urlpatterns = url_reset_password + url_accueil
