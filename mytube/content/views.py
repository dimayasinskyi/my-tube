from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .serializers import VideoSerializer
from .models import Recommendations, Video, Tag


class Home(ListView):
    template_name = "content/home.html"
    context_object_name = "videos"
    paginate_by = 16
    
    def get_videos(self, video):
        param = self.request.GET
        if param.get("search"):
            videos = video.filter(title__icontains=param.get("search")).order_by("title")
        elif param.get("tag"):
            videos = video.filter(tags=param.get("tag")).order_by("tags")
        else:
            videos = video.order_by("-created_at")
        return videos

    def get_queryset(self):

        if self.request.user.is_authenticated:
            user = self.request.user

            serializer = VideoSerializer(self.get_videos(Video.objects.all()), many=True, context={"user": user})
            recommendations = Recommendations.objects.get(user=user)

            recommendations.video.clear()
            video_ids = []

            for serializer in serializer.data:
                if serializer.get("is_liked_by_user")[0]:
                    video_ids.append(serializer.get("video_id"))
                    
            recommendations.video.set(video_ids)
            return Recommendations.objects.get(user=user).video.all()[:50]
        
        return self.get_videos(Video.objects.all())[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all().order_by("title")
        
        querystring = self.request.GET.copy()
        if "page" in querystring:
            del querystring["page"]

        context["querystring"] = f"&{querystring.urlencode()}" if querystring else ""
        return context


class VideoCreateVideo(CreateView):
    model = Video
    fields = ["title", "description", "tags", "file"]
    template_name = "content/create_video.html"
    success_url = reverse_lazy("account:profile")

    def form_valid(self, form):
        form.instance.channel = self.request.user.channel
        return super().form_valid(form)
