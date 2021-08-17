
from api.models import Dish, Menu
from django.http import Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
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


class ListDishes(APIView):
    """
    Retrieve list of dishes or post a new dish
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        dish = Dish.objects.all()
        serializer = DishSerializer(dish, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetail(APIView):
    """
    Retrieve, update or delete a dish instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Dish.objects.get(pk=pk)
        except Dish.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dish = self.get_object(pk)
        serializer = DishSerializer(dish)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dish = self.get_object(pk)
        serializer = DishSerializer(dish, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dish = self.get_object(pk)
        dish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListMenus(APIView):
    """
    Retrieve list of menus or post a new menu
    """
    permission_classes = [IsGetOrIsAuthenticated]

    def get(self, request, format=None):
        menus = Menu.objects.all()
        search_string = request.GET.get('search_title')
        if search_string:
            menus = menus.filter(title__icontains=search_string)
        if 'sort_by' in request.GET:
            if request.GET.get('sort_by') == 'title':
                menus = menus.order_by('title')
            elif request.GET.get('sort_by') == 'dish_count':
                menus = menus.order_by('dish_count')
            else:
                return Response(
                    {
                        "Error": "Value of the parameter 'sort_by' cant be other than 'title' or 'dish_count'",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetail(APIView):
    """
    Retrieve, update or delete a menu instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            menu = Menu.objects.prefetch_related('dishes').get(pk=pk)
        except Menu.DoesNotExist:
            raise Http404
        serializer = MenuDetailSerializer(menu)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        menu = self.get_object(pk)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
