from django.urls import path


from .views import registration, home


app_name = "companies"

url_registration = [
    path("registration/identity", registration.identity, name="identity"),
    path("registration/company", registration.mon_entreprise, name="company"),
    path("registration/mission", registration.mission, name="mission"),
    path("registration/candidat", registration.candidat, name="candidat"),
    path("registration/engagement", registration.engagement, name="engagement"),
]

url_home = [
    path("search", home.search_page, name="search"),
    path("researches", home.researches, name="researches"),
    path("researches/<int:job_pk>", home.researches, name="researches"),
    path("search/<int:job_pk>/", home.search_page, name="search_job"),
    path("likes", home.likes_page, name="likes"),
    path("matches", home.matches_page, name="matches"),
    path(
        "change_research_mission", registration.mission, name="change_research_mission"
    ),
    path(
        "change_research_candidat",
        registration.candidat,
        name="change_research_candidat",
    ),
    path("get/student_card", home.student_card, name="student_card"),
    path("get/likes", home.get_students_that_job_liked, name="get_likes"),
    path(
        "get/likes/students",
        home.get_students_that_liked_job,
        name="get_likes_students",
    ),
    path("get/matches", home.get_matches, name="get_matches"),
    path("message", home.chat_page, name="message"),
    path("delete_profil", home.delete_profil, name="delete_profil"),
    path(
        "get/student/<int:pk>/", home.get_student_infos_page, name="get_student_infos"
    ),
    path("create_job", home.create_job, name="create_job"),
    path(
        "registration/mission/mailMissingPoste",
        home.mailMissingPoste,
        name="mailMissingPoste",
    ),
    path("send_message", home.send_message, name="send_message"),
]

urlpatterns = url_home + url_registration
