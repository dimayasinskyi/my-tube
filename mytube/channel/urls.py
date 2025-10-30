from django.urls import path

from .views import create_channel, ChannelUpdateView, ChannelDetailView


app_name = "channel"

urlpatterns = [
    path("create/", create_channel, name="create_channel"),
    path("profile/<str:pk>/", ChannelUpdateView.as_view(), name="profile_channel"),
    path("view/<str:pk>/", ChannelDetailView.as_view(), name="view_channel"),
]