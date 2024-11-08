from django.shortcuts import render
from userAuth import serializers as api_serializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
    permission_classes = [AllowAny]