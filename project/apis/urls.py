
from django.urls import path
from . import views
urlpatterns = [

    path('search/', views.UserSearchApiView.as_view(), name="search-api"),
    path('send/', views.SendFriendRequestView.as_view(), name="send-request"),
    path('accept/', views.AcceptFriendRequestView.as_view(), name="accept-request"),
    path('reject/', views.RejectFriendRequestView.as_view(), name="reject-request"),
    path('list-accepted', views.ListAcceptedFriendRequestsView.as_view(),
         name="list-accepted"),
    path('list-rejected', views.ListRejectedFriendRequestsView.as_view(),
         name="list-rejected"),
    path('list-pending', views.ListPendingFriendRequestsView.as_view(),
         name="list-pending")
]
