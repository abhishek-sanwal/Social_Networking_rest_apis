from rest_framework.serializers import ModelSerializer

from django.dispatch import Signal
from .models import SocialProfile, AcceptdFriendRequests, RejectedFriendRequests, PendingFriendRequests


class PendingFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = PendingFriendRequests
        fields = ["__all__"]


class RejectedFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = RejectedFriendRequests
        fields = ["__all__"]


class AcceptedFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = AcceptdFriendRequests
        fields = ["__all__"]
