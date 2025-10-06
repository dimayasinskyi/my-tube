from django.urls import path

from .views import VideoCreateView, Home, VideoDetailView


app_name = "content"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("create/video/", VideoCreateView.as_view(), name="create_video"),
    path("<int:pk>/", VideoDetailView.as_view(), name="view_video"),
]