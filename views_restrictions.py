from django.contrib.auth.decorators import user_passes_test

from welcome_pages.models import User


def active_user_required(view_func):
    def check_fn(user: User) -> bool:
        if not user.is_authenticated:
            return False
        return user.is_active

    decorated_view_func = user_passes_test(
        check_fn,
        login_url="/",
    )(view_func)
    return decorated_view_func


def finished_inscription_required(view_func):
    def has_finished_inscription(user: User) -> bool:
        if not user.is_authenticated:
            return False
        return user.finished_inscription

    decorated_view_func = user_passes_test(
        has_finished_inscription,
        login_url="/",
    )(view_func)
    return decorated_view_func


def company_required(view_func):
    def check_fn(user: User) -> bool:
        if not user.is_authenticated:
            return False
        return user.is_company()

    decorated_view_func = user_passes_test(
        check_fn,
        login_url="/",
    )(view_func)
    return decorated_view_func


def student_required(view_func):
    def check_fn(user: User) -> bool:
        if not user.is_authenticated:
            return False
        return user.is_student()

    decorated_view_func = user_passes_test(
        check_fn,
        login_url="/",
    )(view_func)
    return decorated_view_func
