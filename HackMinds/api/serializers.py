from django.contrib.auth.admin import User
from .models import DeckModel, CardModel

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']


class DeckModelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DeckModel
        fields = '__all__'

class CardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CardModel
        fields = '__all__'