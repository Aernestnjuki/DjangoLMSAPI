from .models import User, Profile
from rest_framework.serializers import ModelSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
