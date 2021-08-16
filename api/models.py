from django.db import models

# Create your models here.


class Dish(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    prepare_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_vegetarian = models.BooleanField()


class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    dishes = models.ManyToManyField(Dish)

    def get_dishes_detail(self):
        return Dish.objects.filter(menu=self)
