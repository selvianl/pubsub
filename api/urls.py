from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from api import views

urlpatterns = [
    path('order/', views.Order.as_view(), name='pubsub'),
    path('order/list/', views.OrderList.as_view(), name="orders"),
    path('jwt/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/token/verify/',
         TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
