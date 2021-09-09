from djoser.views import UserViewSet as BaseUserViewSet

from ..services.pagination import LimitPageNumberPagination
from .models import User
from .serializers import UserListSerializer

# from rest_framework.decorators import action


class UserViewSet(BaseUserViewSet):

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = LimitPageNumberPagination
