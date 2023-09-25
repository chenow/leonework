from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class EmailBackend(AllowAllUsersModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
