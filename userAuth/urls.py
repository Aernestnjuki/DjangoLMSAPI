from userAuth import views as api_views
from django.urls import path

# create a token_refresh api view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/token/', api_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/signin/', api_views.SignInAPIView.as_view()),
    path('user/password-reset-email/<email>/', api_views.PasswordEmailVerifyAPIView.as_view()),
    path('user/password-change/', api_views.PasswordChangeAPIView.as_view()),
]
