from django.conf import settings

import requests


class SendInfoOfUser:
    """Sends data about site actions to a Telegram bot."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        data = {}
        # IP
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        data["api"] = ip
        # Device
        data["device"] = request.headers.get('User-Agent')
        # Path, method
        data["path"] = request.build_absolute_uri()
        data["method"] = request.method
        # language
        data["language"] = request.headers.get("Accept-Language")
        # Referer
        data["regerer"] = request.headers.get("Regerer")
        # Status
        data["status"] = response.status_code

        text = "SITE:\n\n\n"
        for key, value in data.items():
            if value:
                text += f"{key}: {value}\n\n"
        requests.post(settings.TELEGRAM_BOT_URL, {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text})

        return response
