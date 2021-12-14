from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'chosen_query_count', 'access')
