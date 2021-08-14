from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Menu, Dish


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['title',
                  'description',
                  'price',
                  'prepare_time',
                  'created_at',
                  'modified_at',
                  'is_vegetarian', ]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['title',
                  'description',
                  'created_at',
                  'modified_at',
                  'dishes', ]
