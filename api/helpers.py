import time
from datetime import datetime

from api.models import Order, OrderStateEnum


def process_order(order_id):
    order = Order.objects.get(id=order_id)
    order.state = OrderStateEnum.PREPARING.value
    order.updated_at = datetime.now()
    order.save(update_fields=["state", "updated"])
    time.sleep(1)
    order.state = OrderStateEnum.READY.value
    order.updated_at = datetime.now()
    order.save(update_fields=["state", "updated"])
    return order
