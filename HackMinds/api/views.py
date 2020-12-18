from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from .models import User
from .serializers import UserSerializer

# Create your views here.
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