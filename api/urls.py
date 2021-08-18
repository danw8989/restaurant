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

    path("dishes/",views.ListDishesAPIView.as_view(),name="dish_list"),
    path("dishes/create/", views.CreateDishAPIView.as_view(),name="dish_create"),
    path("dish/<int:pk>/",views.RetrieveDishAPIView.as_view(),name="retrieve_dish"),
    path("dish/update/<int:pk>/",views.UpdateDishAPIView.as_view(),name="update_dish"),
    path("dish/delete/<int:pk>/",views.DeleteDishAPIView.as_view(),name="delete_dish"),


    path("menus/",views.ListMenuAPIView.as_view(),name="menu_list"),
    path("menus/create/", views.CreateMenuAPIView.as_view(),name="menu_create"),
    path("menu/<int:pk>/",views.RetrieveMenuAPIView.as_view(),name="retrieve_menu"),
    path("menu/update/<int:pk>/",views.UpdateMenuAPIView.as_view(),name="update_menu"),
    path("menu/delete/<int:pk>/",views.DeleteMenuAPIView.as_view(),name="delete_menu")
]

