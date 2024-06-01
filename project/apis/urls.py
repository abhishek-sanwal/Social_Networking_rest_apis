
from django.urls import path
from .views import UserSearchApi
urlpatterns = [

    path('search/', UserSearchApi.as_view(), name="search-api")
]
