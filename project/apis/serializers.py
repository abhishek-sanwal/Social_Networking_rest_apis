from rest_framework.serializers import ModelSerializer

from django.dispatch import Signal
from .models import SocialProfile, AcceptdFriendRequests, RejectedFriendRequests, PendingFriendRequests


class SocialProfileSerializer(ModelSerializer):

    class Meta:

        model = SocialProfile
        fields = ["user"]


class PendingFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = PendingFriendRequests
        fields = ["sender", "receiver", "message", "time"]
        read_only_fields = ["sender", "receiver"]

    def create(self, validated_data):

        request = self.context.get("request")

        user = request.user

        sender_user = SocialProfile.objects.filter(user=user).first()
        print(sender_user, "I am sender user")
        receiver_user = self.context.get("receiver_user")
        print(receiver_user, " I am receiver user")
        return PendingFriendRequests.objects.create(sender=sender_user,
                                                    receiver=receiver_user, **validated_data)


class RejectedFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = RejectedFriendRequests
        fields = ["__all__"]


class AcceptedFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = AcceptdFriendRequests
        fields = ["__all__"]
