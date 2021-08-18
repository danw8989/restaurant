
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
    """Lists all dishes from the database"""
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
class CreateDishAPIView(CreateAPIView):
    """Creates a new dish"""
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class UpdateDishAPIView(UpdateAPIView):
    """Updates dish instance with id provided"""
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DeleteDishAPIView(DestroyAPIView):
    """Deletes dish instance with id provided"""
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class RetrieveDishAPIView(RetrieveAPIView):
    """Retrieves dish instance with id provided"""
    permissions = [permissions.IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class ListMenuAPIView(ListAPIView):
    """Lists all menus from the database"""
    serializer_class = MenuSerializer

    def get_queryset(self):
        menus = Menu.objects.all()
        search_string = self.request.query_params.get('search_title')
        added_string = self.request.query_params.get('created')
        modified_string = self.request.query_params.get('modified')
        if search_string:
            menus = menus.filter(title__icontains=search_string)
        if added_string:
            menus = menus.filter(created_at__gte=added_string)
        if modified_string:
            menus = menus.filter(modified_at__gte=modified_string)
        if 'sort_by' in self.request.query_params:
            if self.request.query_params.get('sort_by') == 'title':
                menus = menus.order_by('title')
            elif self.request.query_params.get('sort_by') == 'dish_count':
                menus = menus.order_by('dish_count')
            else:
                return Response(
                    {
                        "Error": "Value of the parameter 'sort_by' cant be other than 'title' or 'dish_count'",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        #serializer = MenuSerializer(menus, many=True)
        return menus


class CreateMenuAPIView(CreateAPIView):
    """Creates a new menu instance"""
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class UpdateMenuAPIView(UpdateAPIView):
    """Updates menu instance with id provided"""
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class DeleteMenuAPIView(DestroyAPIView):
    """Deletes menu instance with id provided"""
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class RetrieveMenuAPIView(RetrieveAPIView):
    """Retrieves menu instance (with detail) with id provided"""
    permissions = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer