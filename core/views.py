from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core import models as api_models
from userAuth import serializers as api_serilizers

from decimal import Decimal

class CategoryListAPIView(generics.ListAPIView):
    queryset =api_models.Category.objects.all()
    serializer_class = api_serilizers.CategorySerializer
    permission_classes = [AllowAny]

class CourseListApiView(generics.ListAPIView):
    queryset = api_models.Course.objects.filter(platform_status='Published', teacher_course_status='Published')
    serializer_class = api_serilizers.CourseSerialiser
    permission_classes = [AllowAny]

class CourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serilizers.CourseSerialiser
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        course = api_models.Course.objects.get(slug=slug, platform_status='Published', teacher_course_status='Published')
        return course
    
class CartAPIView(generics.CreateAPIView):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serilizers.CartSerializer
    permission_classes = [AllowAny]

    # overridding the default create function
    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']
        user_id = request.data['user_id']
        price = request.data['price']
        country_name = request.data['country_name']
        cart_id = request.data['cart_id']

        # getting the actual course id
        course = api_models.Course.objects.filter(id=course_id).first()
        print("course_id *******:", course_id)

        # check if user exists first before adding product to cart
        if user_id != 'undefined':
            user = api_models.User.objects.filter(id=user_id).first()
        else:
            user = None

        try:
            country_object = api_models.Country.objects.filter(name=country_name).first()
            country = country_object.name
        except:
            country_object = None
            country = 'Japan'

        # get tax_rate of an existing country
        if country_object != None:
            tax_rate = country_object.tax_rate / 100
        else:
            tax_rate = 0

        cart = api_models.Cart.objects.filter(cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.totak = Decimal(price) + Decimal(tax_rate)
            cart.save()

            return Response({"message": "Cart updated Successfully"}, status=status.HTTP_200_OK)
        else:
            cart = api_models.Cart()
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.totak = Decimal(price) + Decimal(tax_rate)
            cart.save()

            return Response({"message": "Cart created Successfully"}, status=status.HTTP_201_CREATED)