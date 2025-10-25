from rest_framework import authentication, exceptions

from core.admin.models import User


class TokenAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None
        
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token")
        
        return (user, None)