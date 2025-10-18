import os, random
from django.conf import settings
from django.contrib.auth import get_user_model

from celery import Celery
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytube.settings")

app = Celery("mytube")
app.config_from_object("django.conf.settings", namespace="CELERY")


@app.task
def create_recommendation(user_id:int, serializers:list):
    """Makes a request to the recommendations microservice, sorts and updates the Recommendations model video."""
    if not serializers:
        print("Serializers is empty.")
        return "Error"
    
    from content.models import Recommendations

    user = get_user_model().objects.get(id=user_id)
    headers = {
        "Authorization": f"Token {settings.RECOMMENDATION_SERVICE_ADMIN_TOKEN}",
        "Host": "localhost",
    }
    response = requests.post(settings.RECOMMENDATION_SERVICE_URL, headers=headers, json=serializers)
    try:
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
        print(f"Recommendation service request error: {e}")
        return "Error"
        
    sorted_data = sorted(response.json(), key=lambda f: (not f["is_liked_by_user"], random.random()))
    Recommendations.objects.get(user=user).video.set([data["video_id"] for data in sorted_data[:50]])
    return f"Recommendation for {user.username} is create."


@app.task
def send_info_user_tg(data:dict):
    """Sends information about requests to the TG bot."""
    text = "SITE:"
    for key, value in data.items():
        if value:
            text += f"\n\n{key}: {value}"
    requests.post(settings.TELEGRAM_BOT_URL, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": text})
    return "Info is send."
