from .models import User, Profile
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# returns an access_token and a refresh_token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add user information in the token
        token['full_name'] = user.full_name
        token['username'] = user.username
        token['email'] = user.email

        return token


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
