from django.urls import path
from rest_framework import routers

from .views import CheckUserViewSet, pay_view

router = routers.SimpleRouter()
router.register(r'webhook', CheckUserViewSet, base_name='xsolla_webhook')

urlpatterns = [
    path('pay', pay_view)
]

urlpatterns += router.urls
