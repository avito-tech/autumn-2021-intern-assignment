from djoser.views import UserViewSet as BaseUserViewSet
# from rest_framework.decorators import action

from .models import User
from .serializers import UserListSerializer
from ..services.pagination import LimitPageNumberPagination


class UserViewSet(BaseUserViewSet):

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = LimitPageNumberPagination
