from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.dispatch import Signal
from .models import SocialProfile, AcceptdFriendRequests, RejectedFriendRequests, \
    PendingFriendRequests


class SocialProfileSerializer(ModelSerializer):

    user = serializers.ReadOnlyField(source='User.email')

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
        print(sender_user, "I am a sender user")
        receiver_user = self.context.get("receiver_user")
        print(receiver_user, " I am a receiver user")
        return PendingFriendRequests.objects.create(sender=sender_user,
                                                    receiver=receiver_user, **validated_data)


class RejectedFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = RejectedFriendRequests
        fields = ["sender", "receiver", "message", "time"]
        read_only_fields = ["sender", "receiver"]

    def create(self, validated_data):

        sender_user = self.context.get("sender")
        print(sender_user, "I am sender user")
        receiver_user = self.context.get("receiver")
        print(receiver_user, " I am receiver user")
        return RejectedFriendRequests.objects.create(sender=sender_user,
                                                     receiver=receiver_user, **validated_data)


class AcceptedFriendRequestsSerializer(ModelSerializer):

    class Meta:

        model = AcceptdFriendRequests
        fields = ["sender", "receiver", "message", "time"]
        read_only_fields = ["sender", "receiver"]

    def create(self, validated_data):

        sender_user = self.context.get("sender")
        print(sender_user, "I am sender user")
        receiver_user = self.context.get("receiver")
        print(receiver_user, " I am receiver user")
        return AcceptdFriendRequests.objects.create(sender=sender_user,
                                                    receiver=receiver_user, **validated_data)
