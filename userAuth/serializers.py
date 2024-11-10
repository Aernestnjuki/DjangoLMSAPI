from .models import User, Profile
from core import models as api_models

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


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
    
class RegistrationSerializer(serializers.ModelSerializer):
    # validating the password when the user registers an account
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            print(attr['password'])
            raise serializers.ValidationError({'Error': 'Password field does not match!'})
        
        return attr
    
    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email']
        )

        email_username, _ = user.email.split('@')
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


############################### Models from Core app #############################

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Category
        fields = [
            'title',
            'image',
            'slug',
            'course_count'
        ]


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Teacher
        fields = ['user', 'image', 'full_name', 'bio', 'facebook', 'linkedin', 'twitter', 'about', 'country', 'students', 'courses', 'review']


class VariantItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.VariantItem
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):

    variant_item = VariantItemSerializer(many=True)

    class Meta:
        model = api_models.Variant
        fields = '__all__'




class Question_Answer_messagesSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Question_Answer_Message
        fields = '__all__'

class Question_AnswerSerializer(serializers.ModelSerializer):

    messages = Question_Answer_messagesSerializer(many=True)
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Question_Answer
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Cart
        fields = '__all__'

class CartOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.CartOrderItem
        fields = '__all__'


class CartOrderSerializer(serializers.ModelSerializer):

    order_itmes = CartOrderItemSerializer(many=True)

    class Meta:
        model = api_models.CartOrder
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Certificate
        fields = '__all__'

class CompletedLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.CompletedLesson
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Note
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    
    prifile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Review
        fields = '__all__'

class EnrolledCourseSerializer(serializers.ModelSerializer):

    lectures = VariantItemSerializer(many=True, read_only=True)
    completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum = VariantSerializer(many=True, read_only=True)
    motes = NoteSerializer(many=True, read_only=True)
    question_answer = Question_AnswerSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = api_models.EnrolledCourse
        fields = '__all__'


class CourseSerialiser(serializers.ModelSerializer):

    student = EnrolledCourseSerializer(many=True)
    curriculum = VariantItemSerializer(many=True)
    lectures = VariantItemSerializer(many=True)

    class Meta:
        model = api_models.Course
        fields = [
            'category',
            'teacher',
            'file',
            'image',
            'title',
            'description',
            'price',
            'languuage',
            'level',
            'platform_status',
            'teacher_course_status',
            'featured',
            'course_id',
            'slug',
            'date',
            'students',
            'curriculum',
            'lectures'
        ]


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Notifications
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Coupon
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.WishList
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Country
        fields = '__all__'


