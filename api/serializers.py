from collections import OrderedDict
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
    def get_mail_description(self):
        return f"Dish name: {self.data.get('title')}\nDescription: {self.data.get('description')}\nPrice: {self.data.get('price')}\nTime to prepare: {self.data.get('prepare_time')}\nVegetarian: {'Yes' if self.data.get('is_vegetarian') else 'No'}\n"
    class Meta:
        model = Dish
        fields = ['id',
                  'title',
                  'description',
                  'price',
                  'prepare_time',
                  'created_at',
                  'modified_at',
                  'is_vegetarian', ]


class MenuSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), many=True)

    class Meta:
        model = Menu

        fields = ['id',
                  'title',
                  'description',
                  'created_at',
                  'modified_at',
                  'dishes',
                  ]


class MenuDetailSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Menu

        fields = ['title',
                  'description',
                  'created_at',
                  'modified_at',
                  'dishes',
                  ]
