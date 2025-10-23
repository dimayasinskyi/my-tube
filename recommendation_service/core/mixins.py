from bson import ObjectId


class MongoMixin:
    """Adapts methods: get_queryset, get_object for working with the model mongodb"""
    model = None
    context_object_name = None

    def get_queryset(self):
        return self.model.objects.all()
    
    def get_object(self):
        id = self.kwargs.get("id")
        if id:
            return self.model.objects(id=ObjectId(id))