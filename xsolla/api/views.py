import hashlib

import pymongo
from django.conf import settings
from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Pay, User
from .serializers import UserCheckSerializer
from .utils import MERCHANT_ID, PROJECT_ID, SECRET_KEY, get_token


def pay_view(request):
    token = get_token()
    return render(request, 'pay.html', {'access_token': token})


class MongoStorage:
    def __init__(self):
        client = pymongo.MongoClient(settings.MONGO_URI)
        self.db = client['payments']
        self.collection = self.db['pays']

    def save(self, document):
        self.collection.insert_one(document)

    def update(self, filter, field, value):
        self.collection.update_one(filter, {'$set': {field: value}})


class CheckUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserCheckSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '').split()
        valid_signature = hashlib.sha1(request.stream.body + SECRET_KEY.encode()).hexdigest()
        if len(auth_header) != 2 or auth_header[1] != valid_signature:
            response_data = {"error": {"code": "INVALID_SIGNATURE", "message": "Invalid signature"}}
            return Response(response_data, status.HTTP_400_BAD_REQUEST)

        data = request.data
        storage = MongoStorage()

        notification_type = data['notification_type']
        if notification_type == 'order_canceled':
            Pay.objects.filter(order_id=data['order']['id']).update(canceled=True)
            storage.update({'order.id': data['order']['id']}, 'order.status', data['order']['status'])
            return Response(status=status.HTTP_204_NO_CONTENT)

        elif notification_type == 'order_paid':
            Pay.objects.update_or_create(
                order_id=data['order']['id'], user=User.objects.last(), defaults={'canceled': False}
            )
            storage.save(data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        elif notification_type == 'user_validation':
            user_id = data['user']['id']
            if not User.objects.filter(player_id=user_id).exists():
                response_data = {"error": {"code": "INVALID_USER", "message": "Invalid user"}}
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_200_OK)

        elif notification_type == 'payment':
            if data['settings']['project_id'] == PROJECT_ID and data['settings']['merchant_id'] == MERCHANT_ID:
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
