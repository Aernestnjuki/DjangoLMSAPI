from userAuth import views as auth_views
from core import views as core_views
from django.urls import path

# create a token_refresh api view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication urls
    path('user/token/', auth_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/signin/', auth_views.SignInAPIView.as_view()),
    path('user/password-reset-email/<email>/', auth_views.PasswordEmailVerifyAPIView.as_view()),
    path('user/password-change/', auth_views.PasswordChangeAPIView.as_view()),

    # core app urls
    path('course/category/', core_views.CategoryListAPIView.as_view()),
    path('course/course-list/', core_views.CourseListApiView.as_view()),
    path('course/course-detail/<slug>/', core_views.CourseDetailAPIView.as_view()),
]
