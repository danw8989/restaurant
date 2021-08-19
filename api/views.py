
from api.filters import MenuFilter
from django_filters import rest_framework as filters
from rest_framework import generics
from api.models import Dish, Menu
from django.http import Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from api.serializers import DishSerializer, MenuDetailSerializer, MenuSerializer, UserSerializer, GroupSerializer
from .perms import IsGetOrIsAuthenticated
from django.db.models import Count


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListDishesAPIView(ListAPIView):
    """
    Lists all dishes from the database
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class CreateDishAPIView(CreateAPIView):
    """
    Creates a new dish
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class UpdateDishAPIView(UpdateAPIView):
    """
    Updates dish instance with id provided
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DeleteDishAPIView(DestroyAPIView):
    """
    Deletes dish instance with id provided
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class RetrieveDishAPIView(RetrieveAPIView):
    """
    Retrieves dish instance with id provided
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class ListMenuAPIView(ListAPIView):
    """
    Lists all menus from the database\n
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    #filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MenuFilter


class CreateMenuAPIView(CreateAPIView):
    """
    Creates a new menu instance
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class UpdateMenuAPIView(UpdateAPIView):
    """
    Updates menu instance with id provided
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class DeleteMenuAPIView(DestroyAPIView):
    """
    Deletes menu instance with id provided
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class RetrieveMenuAPIView(RetrieveAPIView):
    """
    Retrieves menu instance (with detail) with id provided
    """
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer
