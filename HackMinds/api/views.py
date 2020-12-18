# Django
from django.shortcuts import render

# Django REST Framwork
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Models
from .models import User, DeckModel, CardModel

# Serializers
from .serializers import UserSerializer, DeckModelSerializer, CardModelSerializer

@api_view(['POST'])
@permission_classes([])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        User.objects.create_user(
            username=serializer.initial_data['username'],
            password=serializer.initial_data['password']
            )
        user = User.objects.get(username=serializer.data['username'])
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key
        },status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data       = request.data
        serializer = DeckModelSerializer(data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
    def get(self, request):
        decks      = DeckModel.objects.filter(id_user=request.user)
        DeckModelSerializer(decks)

class CardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data       = request.data
        serializer = CardModelSerializer(data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def get(self, request, id):
        cards      = CardModel.objects.filter(id_deck=id)
        CardModelSerializer(cards)