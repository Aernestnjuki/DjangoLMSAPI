from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny

from core import models as api_models
from userAuth import serializers as api_serilizers

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