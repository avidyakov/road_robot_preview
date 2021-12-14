import logging

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer
from .models import User
from question_app.actors import send_message


logger = logging.getLogger(__name__)


class CreateUser(generics.CreateAPIView):
    queryset = User
    serializer_class = UserSerializer


class RetrieveUpdateUser(generics.RetrieveUpdateAPIView):
    queryset = User
    serializer_class = UserSerializer


class PaymentHook(APIView):

    def post(self, request, format=None):
        try:
            status = request.data['bill']['status']['value']
            user_id = request.data['bill']['billId']
        except KeyError:
            logger.error(request.data)
            raise ParseError

        if status == 'PAID':
            user = get_object_or_404(User, pk=user_id)
            if not user.payment:
                user.payment = True
                user.save()
                send_message.send(user.id, 'Спасибо за покупку! Теперь у вас есть полный доступ к боту!')

        return Response()
