import json

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
from pubsub.settings import pub

from api.models import (
    Food, Order, OrderStateEnum,
    Restaurant, RestaurantCategory
)

AUTH_USER_MODEL = User


class UserSignUpTestCase(TransactionTestCase):
    reset_sequences = True
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        rest_cat = baker.make(RestaurantCategory, name='test')
        res = baker.make(Restaurant, name="test", category=rest_cat)
        baker.make(Food, id=1, name='test', restaurant=res)

        cls.user = baker.prepare(User, username="root", password='toor')
        cls.user.set_password(cls.user.password)
        cls.user.save()
        cls.url = reverse('pubsub')
        cls.login_url = reverse('token_obtain_pair')
        cls.client = APIClient()

    def test_pubsub(self):
        payload = {
            "username": 'root',
            "password": 'toor'
        }
        resp = self.client.post(self.login_url, payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        content = json.loads(resp.content)

        # Prepare data
        data = {
            'food_id': 1,
        }

        # Publish to redis
        resp = self.client.post(
            self.url, data, content_type="application/json",
            **{'HTTP_AUTHORIZATION': f"Bearer {content['access']}"},
            follow=True
        )
        # Check status response and db
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        self.assertEqual(Order.objects.filter(
            id=json.loads(resp.content)['order']).exists(), True
        )
        self.assertEqual(Order.objects.get(
            id=json.loads(resp.content)['order']).state,
            OrderStateEnum.GETTED.value
        )

        # Check redis
        message = pub.get_message()
        if message:
            self.assertEqual(message['data'], data['food_id'])
