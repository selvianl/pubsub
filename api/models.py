from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class OrderStateEnum(Enum):
    GETTED = "GETTED"
    PREPARING = "PREPARING"
    READY = "READY"

    @classmethod
    def choices(cls):
        return [(i, i.value) for i in cls]


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=255)


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(RestaurantCategory, on_delete=models.PROTECT)


class Food(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    state = models.CharField(
        max_length=50,
        choices=OrderStateEnum.choices(),
        default=OrderStateEnum.GETTED.value
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
