from rest_framework import authentication, exceptions

from core.admin.models import User
from core.mongo_sessions_backend import SessionStore


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
    

class SessionAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        session_key = request.COOKIES.get("sessionid") or request.headers.get("X-Session-Id")
        print(session_key)
        if not session_key:
            return None
        
        try:
            session = SessionStore(session_key=session_key).load()
        except Exception:
            raise exceptions.AuthenticationFailed(f"Invalid session")
        
        try:
            user = User.objects.get(id=session.get("user_id"))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
        
        return (user, None)