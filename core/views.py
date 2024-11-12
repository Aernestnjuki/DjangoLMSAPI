from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core import models as api_models
from userAuth import serializers as api_serilizers

from decimal import Decimal
import math

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

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']
        user_id = request.data['user_id']
        price = request.data['price']
        country_name = request.data['country_name']
        cart_id = request.data['cart_id']

        course = api_models.Course.objects.filter(id=course_id).first()

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

        if country_object != None:
            tax_rate = country_object.tax_rate / 100
        else:
            tax_rate = 3 / 100

        cart = api_models.Cart.objects.filter(cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
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
        
class CartListAPIView(generics.ListAPIView):
    serializer_class = api_serilizers.CartSerializer
    permission_classes = [AllowAny]
    queryset = api_models.Cart.objects.all()

class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = api_serilizers.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']

        return api_models.Cart.objects.filter(cart_id=cart_id, id=item_id).first()
    
class CartStatsAPIView(generics.RetrieveAPIView):
    serializer_class = api_serilizers.CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = api_models.Cart.objects.filter(user=user_id)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_price = 0.00
        total_tax = 0.00
        total_total = 0.00

        for cart_item in queryset:
            total_price += float(cart_item.price)
            total_tax += float(cart_item.tax_fee)
            total_total += round(float(cart_item.totak), 2)

        data = {
            'price': total_price,
            'tax': total_tax,
            'total': total_total
        }

        return Response(data, status=status.HTTP_200_OK)

class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = api_serilizers.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()

    def create(self, request, *args, **kwargs):
        full_name = request.data['full_name']
        email = request.data['email']
        country = request.data['country']
        cart_id = request.data['cart_id']
        user_id = request.data['user_id']

        if user_id != 0:
            user = api_models.User.objects.get(id=user_id)
        else:
            user = None

        cart_item = api_models.Cart.objects.filter(cart_id=cart_id)

        total_price = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)

        order = api_models.CartOrder.objects.create(
            full_name=full_name,
            email=email,
            country=country,
            student=user
        )

        for c in cart_item:
            api_models.CartOrderItem.objects.create(
                order=order,
                course=c.course,
                price=c.price,
                tax_fee=c.tax_fee,
                total=c.totak,
                initial_total=c.totak,
                teacher= c.course.teacher
            )

            total_price += Decimal(c.price)
            total_tax += Decimal(c.tax_fee)
            total_initial_total += Decimal(c.totak)
            total_total = Decimal(c.totak)

            order.teacher.add(c.course.teacher)
        
        order.sub_total = total_price
        order.tax_fee = total_tax
        order.total = total_total
        order.initial_total = total_initial_total
        order.save()

        return Response({"Message": "Order Created successfully"}, status=status.HTTP_201_CREATED)

class CheckOutAPIView(generics.RetrieveAPIView):
    serializer_class = api_serilizers.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()
    lookup_field = 'oid'