from django.conf import settings
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from mytube.celery import create_recommendation
from .models import Recommendations, Video, Tag
from .serializers import VideoSerializer
from .forms import VideoCreateForm


class Home(ListView):
    """Recommendations page if the user is registered, if not a selection of random videos."""
    template_name = "content/home.html"
    context_object_name = "videos"
    paginate_by = 16
    
    def get_videos(self, video):
        """Filters and order videos by parameters in requests."""
        param = self.request.GET
        if param.get("search"):
            videos = video.filter(title__icontains=param.get("search")).order_by("title")
        elif param.get("tag"):
            videos = video.filter(tags=param.get("tag")).order_by("tags")
        else:
            videos = video.order_by("-created_at")
        return videos

    def get_queryset(self):
        """
        If any search parameters are passed that have been processed by the get_videos method,
        it simply returns them or, if the user is not authorized, otherwise shows personalized
        recommendations for the user and creates a task to update them.
        """
        if (self.request.GET.get("search") or self.request.GET.get("tag")) or not self.request.user.is_authenticated:
            return self.get_videos(Video.objects.all())[:50]

        user = self.request.user
        serializer = VideoSerializer(self.get_videos(Video.objects.all()), many=True, context={"user": user})
        recommendations = Recommendations.objects.get(user=user).video.all()
        create_recommendation(user, serializer)
        return recommendations
        
    def get_context_data(self, **kwargs):
        """Creates a parameter for page pagination."""
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all().order_by("title")
        
        querystring = self.request.GET.copy()
        if "page" in querystring:
            del querystring["page"]

        context["querystring"] = f"&{querystring.urlencode()}" if querystring else ""
        return context


class VideoCreateVideo(CreateView):
    """Presenting a form VideoCreateForm for creating a video"""
    model = Video
    form_class = VideoCreateForm
    template_name = "content/create_video.html"
    success_url = reverse_lazy("account:profile")

    def form_valid(self, form):
        """Transfers the feed automatically to the form."""
        form.instance.channel = self.request.user.channel
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Breadcrumb navigation."""
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {"name": "Home", "url": reverse_lazy("content:home")},
            {"name": "User profile", "url": reverse_lazy("account:profile", args=[self.request.user.pk])},
            {"name": "Channel profile", "url": reverse_lazy("channel:profile_channel", args=[self.request.user.channel.pk])},
            {"name": "Create video", "url": ""}
            ]
        return context 