from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from huscy.users.serializer import UserSerializer

User = get_user_model()


class ReadOnlyForNonAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.method in SAFE_METHODS


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.order_by('last_name', 'first_name')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, ReadOnlyForNonAdmin)
