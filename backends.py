from django.contrib.auth.models import User

class CaseInsensitiveModelBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None