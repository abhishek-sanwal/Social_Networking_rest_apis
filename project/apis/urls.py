
from django.urls import path
from . import views
urlpatterns = [

    path('search/', views.UserSearchApi.as_view(), name="search-api"),
    path('send/', views.SendFriendRequest.as_view(), name="send-request")
]
