import json

from pubsub.settings import CHANNEL, pub, redis
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.helpers import process_order
from api.models import Order as OrderDB
from api.serializers import OrderBodySerializer, OrderListSerailizer


class Order(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        message = pub.get_message()
        if message:
            try:
                resp = json.loads(message['data'])
                order = process_order(resp['order'])
                resp = {
                    "order_id": order.id,
                    "food_id": order.food_id,
                    "user_id": order.user_id,
                    "state": order.state
                }
                return Response(data=resp)
            except TypeError as exc:
                print(exc)
        return Response(
            data={"detail": "No data"},
            status=status.HTTP_404_NOT_FOUND
        )

    def post(self, request):
        data = request.data
        ser = OrderBodySerializer(
            data=data, context={'request': request}
        )
        ser.is_valid(raise_exception=True)
        order_id = ser.save()
        order = json.dumps({"order": order_id})
        redis.publish(CHANNEL, order)
        return Response(
            data={"order": order_id},
            status=status.HTTP_201_CREATED
        )


class OrderList(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderListSerailizer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = OrderDB.objects.filter(
            user_id=user_id
        )
        return queryset
