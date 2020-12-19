# Django
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist


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
        serializer = DeckModelSerializer(data = data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        decks      = request.user.decks
        return Response(DeckModelSerializer(decks, many = True).data, status.HTTP_200_OK)

class CardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        deck       = DeckModel.objects.get(id = id)
        data       = request.data
        serializer = CardModelSerializer(data = data)
        if serializer.is_valid():
            serializer.save(deck = deck)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        if DeckModel.objects.filter(id=id).exists():
            deck  = DeckModel.objects.get(id = id)
            cards = deck.cards
            return Response (CardModelSerializer(cards, many = True).data, status.HTTP_200_OK)
        else:
            return Response({'error': f'There is no Deck with id:{id}'}, status.HTTP_404_NOT_FOUND)