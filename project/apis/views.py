from django.shortcuts import render

from .serializers import PendingFriendRequestsSerializer, \
    AcceptedFriendRequestsSerializer, RejectedFriendRequestsSerializer

# Create your views here.
from rest_framework.generics import CreateAPIView


class SendFriendRequest(CreateAPIView):

    serializer_class = PendingFriendRequestsSerializer


class AcceptFriendRequest(CreateAPIView):

    serializer_class = AcceptedFriendRequestsSerializer


class RejectFriendRequest(CreateAPIView):

    serializer_class = RejectedFriendRequestsSerializer
