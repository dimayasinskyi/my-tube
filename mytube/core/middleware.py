from mytube.celery import send_info_user_tg


class SendInfoOfUser:
    """Sends data about site actions to a Telegram bot."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        send_info_user_tg(request, response)
        return response
