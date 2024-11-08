from django.shortcuts import render
import random
from userAuth import serializers as api_serializer
from .models import User, Profile

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail
from api.settings import EMAIL_HOST_USER

# recipent_list = [email]

# send_mail(subject, message, Email_host_user, recipient_list, fail_silently=True)

# login view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


# sighin view
class SignInAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegistrationSerializer


# generate random otp
def generate_random_otp(length=7):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp


# create otp and resfresh token in the database
class PasswordEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user = User.objects.filter(email=email).first()

        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"

            print('link:', link)

        return user
