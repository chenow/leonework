from django.urls import path


from . import views

app_name = "matching"


urlpatterns = [
    path("likes/create_like/student/<int:pk>/", views.create_like, name="create_like"),
    path(
        "likes/create_like/company/<int:student_pk>/",
        views.create_like_company,
        name="create_like_company",
    ),
    path(
        "messages/get/<str:user_type>/<int:pk>/",
        views.get_messages,
        name="get_messages",
    ),
    path(
        "messages/get/card/<str:user_type>/<int:pk>/",
        views.get_card_infos,
        name="get_card_info",
    ),
]
