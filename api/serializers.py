from rest_framework import serializers
from rest_framework.status import HTTP_404_NOT_FOUND

from api.models import Order, Food


class OrderBodySerializer(serializers.Serializer):
    food_id = serializers.IntegerField()

    def validate_food_id(self, food_id):
        try:
            Food.objects.get(id=food_id)
            return food_id
        except Food.DoesNotExist:
            raise serializers.ValidationError(
                "Food not found", code=HTTP_404_NOT_FOUND)

    def save(self):
        food_id = self.validated_data['food_id']
        order = Order.objects.create(
            food_id=food_id, user_id=self.context['request'].user.id
        )
        return order.id


class OrderListSerailizer(serializers.ModelSerializer):
    food_name = serializers.SerializerMethodField('food_id')

    def food_id(self, data):
        return (data.food.id, data.food.name)

    class Meta:
        model = Order
        fields = (
            "food_name",
            "user_id",
            "state",
            "created",
            "updated"
        )
