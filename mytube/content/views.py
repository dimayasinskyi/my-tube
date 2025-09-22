from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .serializers import VideoSerializer
from .models import Recommendations, Video, Tag


class Home(ListView):
    template_name = "content/home.html"
    context_object_name = "videos"
    paginate_by = 16

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            serializer = VideoSerializer(Video.objects.order_by("?")[:50], many=True, context={"user": user})
            recommendations = Recommendations.objects.get(user=user)

            recommendations.video.clear()
            video_ids = []

            for serializer in serializer.data:
                if serializer.get("is_liked_by_user")[0]:
                    video_ids.append(serializer.get("video_id"))
                    
            recommendations.video.set(video_ids)
            return Recommendations.objects.get(user=user).video.all().order_by("?")
        
        return Video.objects.order_by("?")[:100]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all().order_by("title")
        return context


class VideoCreateVideo(CreateView):
    model = Video
    fields = ["title", "description", "tags", "file"]
    template_name = "content/create_video.html"
    success_url = reverse_lazy("account:profile")

    def form_valid(self, form):
        form.instance.channel = self.request.user.channel
        return super().form_valid(form)
