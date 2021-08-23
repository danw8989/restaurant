from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("dishes/", views.ListDishesAPIView.as_view(), name="dish_list"),
    path("dishes/create/", views.CreateDishAPIView.as_view(), name="dish_create"),
    path("dish/<int:pk>/", views.RetrieveUpdateDestroyDishAPIView.as_view(),
         name="retrieve_dish"),

    path("menus/", views.ListMenuAPIView.as_view(), name="menu_list"),
    path("menus/create/", views.CreateMenuAPIView.as_view(), name="menu_create"),
    path("menu/<int:pk>/", views.RetrieveUpdateDestroyMenuAPIView.as_view(),
         name="retrieve_menu"),

]
