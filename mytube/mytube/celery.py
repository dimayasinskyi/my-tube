import os
from django.conf import settings

from celery import Celery
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytube.settings")

app = Celery("mytube")
app.config_from_object("django.conf.settings", namespace="CELERY")


@app.task
def create_recommendation(user, serializers):
    """Makes a request to the recommendations microservice, sorts and updates the Recommendations model video."""
    from content.models import Recommendations

    response = requests.post(settings.RECOMMENDATION_SERVICE_URL, json=serializers.data)
    sorted_data = sorted(response.json(), key=lambda f: f["is_liked_by_user"], reverse=True)
    Recommendations.objects.get(user=user).video.set([data["video_id"] for data in sorted_data[:50]])
    return f"Recommendation for {user.username} is create."


@app.task
def send_info_user_tg(request, response):
    """Sends information about requests to the TG bot."""
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
    text = "SITE:"
    for key, value in data.items():
        if value:
            text += f"\n\n{key}: {value}"
    requests.post(settings.TELEGRAM_BOT_URL, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": text})
    return "Info is send."
