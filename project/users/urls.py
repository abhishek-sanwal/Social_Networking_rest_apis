
from django.urls import path
import django.contrib.auth.views as auth_views

from . import views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('signup/', views.signup, name="signup"),
    path('', views.home, name="Homepage")
]
