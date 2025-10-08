from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin:
    """Checks if the object is owned by a user by the variable: owner_field = 'user'."""
    owner_field = "user"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if getattr(obj, self.owner_field) != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)