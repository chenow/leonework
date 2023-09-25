from django.urls import path


from .views import registration, submits, mails, home


app_name = "students"


url_registration = [
    path("registration/identity", registration.identity, name="identity"),
    path("registration/parcours", registration.parcours, name="parcours"),
    path("registration/atouts", registration.atouts, name="atouts"),
    path("registration/mission", registration.mission, name="mission"),
    path("registration/company", registration.company, name="company"),
]

url_submits = [
    path(
        "registration/experiences/select",
        submits.select_experiences,
        name="select_experiences",
    ),
    path("registration/experiences/add", submits.add_experience, name="add_experience"),
    path(
        "registration/experiences/delete/<int:experience>",
        submits.delete_experience,
        name="delete_experience",
    ),
    path("registration/atouts/langs", submits.langs, name="langs"),
    path("registration/atouts/get_langs", submits.get_langs, name="get_langs"),
    path("registration/atouts/qualities", submits.qualities, name="qualities"),
    path(
        "registration/atouts/get_qualities", submits.get_qualities, name="get_qualities"
    ),
    path("registration/atouts/valeurs", submits.valeurs, name="valeurs"),
    path("registration/atouts/get_valeurs", submits.get_valeurs, name="get_valeurs"),
    path("registration/company/get_cities", submits.get_cities, name="get_cities"),
    path("registration/company/save_cities", submits.save_cities, name="save_cities"),
]

url_mails = [
    path(
        "registration/mission/mailMissingMetier",
        mails.mailMissingMetier,
        name="mailMissingMetier",
    ),
    path(
        "registration/mission/mailMissingDiplome",
        mails.mailMissingDiplome,
        name="mailMissingDiplome",
    ),
]

url_home = [
    path("search", home.search, name="search"),
    path("likes", home.likes, name="likes"),
    path("matches", home.matches, name="matches"),
    path("change_search", home.change_search, name="change_search"),
    path(
        "change_research_mission",
        home.change_research_mission,
        name="change_research_mission",
    ),
    path(
        "change_research_entreprise",
        home.change_research_entreprise,
        name="change_research_entreprise",
    ),
    path("get/entreprise_card", home.entreprise_card, name="entreprise_card"),
    path("get/likes", home.get_jobs_that_student_liked, name="get_likes"),
    path("get/likes/ent", home.get_jobs_that_liked_student, name="get_likes_ent"),
    path("get/matches", home.get_matches, name="get_matches"),
    path("message", home.chat, name="message"),
    path("delete_profil", home.delete_profil, name="delete_profil"),
    path("get/company/<int:pk>/", home.get_company_infos, name="get_company_infos"),
    path("send_message", home.send_message, name="create_message"),
]


urlpatterns = url_registration + url_submits + url_mails + url_home
