
from . import views
from django.urls import path
import django.contrib.auth.views as auth_views

from .views import MyObtainTokenPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('signup/', views.signup, name="signup"),
    path('signup2/', views.SignupApi.as_view(), name="signup-api"),
    path('login1/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.home, name="Homepage"),
]
