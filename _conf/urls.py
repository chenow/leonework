from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("administration/", admin.site.urls),
    path("", include("welcome_pages.urls")),
    path("home/", include("home.urls")),
    path("students/", include("students.urls")),
    path("companies/", include("companies.urls")),
    path("matching/", include("matching.urls")),
    path("payment/", include("payment.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="welcome_pages/passwords/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="welcome_pages/passwords/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="welcome_pages/passwords/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="welcome_pages/passwords/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "welcome_pages.views.error_404_view"
handler500 = "welcome_pages.views.error_500_view"
