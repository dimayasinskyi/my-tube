from django.urls import path

from .views import VideoCreateVideo, Home


app_name = "content"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("create/video/", VideoCreateVideo.as_view(), name="create_video"),
]