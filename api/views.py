
from api.perms import IsGetOrIsAuthenticated
from api.filters import MenuFilter
from django_filters import rest_framework as filters
from rest_framework import generics
from api.models import Dish, Menu
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from django.contrib.auth.decorators import login_required
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from api.serializers import DishSerializer, MenuDetailSerializer, MenuSerializer, UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ListDishesAPIView(ListAPIView):
    """
    Lists all dishes from the database
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permissions_classes = [permissions.AllowAny]


class CreateDishAPIView(CreateAPIView):
    """
    Creates a new dish
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class RetrieveUpdateDestroyDishAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


# ----------------------------------------------------------
# MENUS

class ListMenuAPIView(ListAPIView):
    """
    Lists all menus from the database\n
    """
    permission_classes = [permissions.AllowAny]

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    #filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MenuFilter


class CreateMenuAPIView(CreateAPIView):
    """
    Creates a new menu instance
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class RetrieveUpdateDestroyMenuAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsGetOrIsAuthenticated, ]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = MenuDetailSerializer
        return super().retrieve(request, *args, **kwargs)
