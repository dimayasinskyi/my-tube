from core.admin.models import User


class SessionVerificationUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get("user_id")
        user = User.objects(id=user_id).first() if user_id else None
        if user:
            request.user = user
            request.user.is_authenticated = True
            
        response = self.get_response(request)
        return response