from .models import Menu, Dish

from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

import json
from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone


class DishTestCases(APITestCase):

    def create_user(self):
        self.username = "test_admin"
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user

    def login(self):
        self.create_user()
        self.client.login(username=self.username, password=self.password)

    def add_test_dish(self):
        sample_dish = Dish(id=1, title='test', description='testest',
                           price=32.56, prepare_time='00:50:30', is_vegetarian=True)
        sample_dish.save()

    def test_post_dish(self):
        data = json.dumps({
            "title": "test",
            "description": "test_test",
            "price": "43.99",
            "prepare_time": "00:30:00",
            "is_vegetarian": True,
        })
        response = self.client.post(
            '/api/dishes/create/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.login()
        response = self.client.post(
            '/api/dishes/create/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_dishes(self):
        response = self.client.get('/api/dishes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.login()
        response = self.client.get('/api/dishes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_dish(self):
        self.add_test_dish()
        response = self.client.delete('/api/dish/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.login()
        response = self.client.delete('/api/dish/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_dish(self):
        self.add_test_dish()
        response = self.client.get('/api/dish/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.login()
        response = self.client.get('/api/dish/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_dish(self):
        self.add_test_dish()

        data = json.dumps({
            "title": "test2",
            "description": "test_test",
            "price": "43.99",
            "prepare_time": "00:30:00",
            "is_vegetarian": True,
        })
        response = self.client.put(
            '/api/dish/1/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.login()
        response = self.client.put(
            '/api/dish/1/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MenuTestCase(APITestCase):
    def create_user(self):
        self.username = "test_admin"
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user

    def login(self):
        self.create_user()
        self.client.login(username=self.username, password=self.password)

    def add_test_menu(self):
        sample_dish = Dish(id=1, title='test', description='testest',
                           price=32.56, prepare_time='00:50:30', is_vegetarian=True)
        sample_dish.save()
        sample_menu = Menu(id=1, title='test_menu',
                           description='testest')
        sample_menu.dishes.add(sample_dish.id)
        sample_menu.save()

    def test_post_menu(self):

        data = json.dumps({
            "title": "test2",
            "description": "test_test",
            "dishes": [1]
        })

        sample_dish = Dish(id=1, title='test', description='testest',
                           price=32.56, prepare_time='00:50:30', is_vegetarian=True)
        sample_dish.save()
        self.assertEqual(Dish.objects.count(), 1)

        response = self.client.post(
            '/api/menus/create/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login()

        response = self.client.post(
            '/api/menus/create/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_menus(self):
        response = self.client.get('/api/menus/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.login()
        response = self.client.get('/api/menus/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_menu(self):
        self.add_test_menu()
        response = self.client.delete('/api/menu/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.login()
        response = self.client.delete('/api/menu/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_menu(self):
        self.add_test_menu()
        response = self.client.get('/api/menu/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.login()
        response = self.client.get('/api/menu/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_menu(self):
        self.add_test_menu()
        data = json.dumps({
            "title": "teswerwert2",
            "description": "test_test",
            "dishes": [1]
        })
        response = self.client.put(
            '/api/menu/1/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.login()

        response = self.client.put(
            '/api/menu/1/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_title(self):
        self.add_test_menu()
        response = self.client.get('/api/menus/?title_search=test')
        self.assertEqual(len(response.json()), 1)
        response = self.client.get('/api/menus/?title_search=ata')
        self.assertEqual(len(response.json()), 0)

    def test_created_at(self):
        self.add_test_menu()
        now = datetime.now(tz=get_current_timezone())
        response = self.client.get(
            f"/api/menus/?created_at={now.strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 1)
        response = self.client.get(
            f"/api/menus/?created_at={(now - timedelta(days=1)).strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(
            f"/api/menus/?created_at_gt={(now - timedelta(days=1)).strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(
            f"/api/menus/?created_at_lt={(now + timedelta(days=1)).strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 1)

    def test_modified_at(self):
        self.add_test_menu()
        now = datetime.now(tz=get_current_timezone())
        response = self.client.get(
            f"/api/menus/?modified_at={now.strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 1)
        response = self.client.get(
            f"/api/menus/?modified_at={(now - timedelta(days=1)).strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(
            f"/api/menus/?modified_at_gt={(now - timedelta(days=1)).strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(
            f"/api/menus/?modified_at_lt={(now + timedelta(days=1)).strftime('%Y-%m-%d')}")
        self.assertEqual(len(response.json()), 1)

    def test_order(self):
        Menu.objects.create(id=1, title='a',
                            description='a')
        Menu.objects.create(id=2, title='c',
                            description='c')
        Menu.objects.create(id=3, title='b',
                            description='b')

        response = self.client.get("/api/menus/?order_by=title")
        self.assertEqual(response.json()[0]['title'], 'a')
        self.assertEqual(response.json()[2]['title'], 'c')

        response = self.client.get("/api/menus/?order_by=-title")
        self.assertEqual(response.json()[0]['title'], 'c')
        self.assertEqual(response.json()[2]['title'], 'a')
