from mytube.celery import send_info_user_tg


class SendInfoOfUser:
    """Sends data about site actions to a Telegram bot."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        data = {
            "ip": ip,
            "device": request.headers.get("User-Agent"),
            "path": request.build_absolute_uri(),
            "method": request.method,
            "language": request.headers.get("Accept-Language"),
            "regerer": request.headers.get("Regerer"),
            "status": response.status_code,
        }
        send_info_user_tg.delay(data)
        return response
