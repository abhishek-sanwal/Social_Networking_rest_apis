import json
import re

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .serializers import PendingFriendRequestsSerializer, \
    AcceptedFriendRequestsSerializer, RejectedFriendRequestsSerializer, \
    SocialProfileSerializer

from .models import SocialProfile, PendingFriendRequests, AcceptdFriendRequests, \
    RejectedFriendRequests

from .paginators import SmallResultsSetPagination
from .throttlers import SendApiThrottle


class UserSearchApiView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_classes = SmallResultsSetPagination

    def get(self, request):

        #  IF search word is not provided
        if "search_word" not in request.data:
            data = " Either email or username is required to search"
            return Response(json.dumps(data), status=status.HTTP_400_BAD_REQUEST)

        search_word = request.data["search_word"]
        # print(search_word)
        # If search_word is a email
        email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        match = re.search(email_pattern, search_word)
        if match is not None:
            search_word = search_word.lower()
            social_user = SocialProfile.objects.filter(
                user__email__exact=search_word)

            if not social_user:
                social_user = SocialProfile.objects.filter(
                    user__email__contains=search_word[:search_word.find("@")])

            serializer = SocialProfileSerializer(social_user, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Else search_word is a username
        else:

            print(search_word, "This is search word")
            social_user = SocialProfile.objects.filter(
                user__username__exact=search_word).first()
            print(social_user, social_user is None)
            if not social_user:
                print("Contains")
                social_user = SocialProfile.objects.filter(
                    user__username__contains=search_word)

            serializer = SocialProfileSerializer(social_user, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)


class SendFriendRequestView(generics.CreateAPIView):

    serializer_class = PendingFriendRequestsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [SendApiThrottle]

    def post(self, request):

        print(request.data)
        email = request.data["email"].lower()
        print("email received")
        receiver_user = SocialProfile.objects.filter(
            user__email__exact=email).first()
        print(receiver_user)
        if receiver_user is None:
            data = "Provided email is not a valid user"
            return Response(json.loads(data), status=status.HTTP_400_BAD_REQUEST)

        sender_user = SocialProfile.objects.filter(user=request.user).first()

        accepted_friend_request = AcceptdFriendRequests.objects.filter(
            Q(sender=sender_user) & Q(receiver=receiver_user)).first()

        rejected_friend_request = RejectedFriendRequests.objects.filter(
            Q(sender=sender_user) & Q(receiver=receiver_user)).first()

        pending_friend_request = PendingFriendRequests.objects.filter(
            Q(sender=sender_user) & Q(receiver=receiver_user)).first()

        print(accepted_friend_request,
              pending_friend_request, rejected_friend_request)
        # If friend request is already accepted.
        if accepted_friend_request is not None:

            return Response(json.dumps("You are already friends"), status=status.HTTP_400_BAD_REQUEST)

        # If friend request is already rejected.
        if rejected_friend_request is not None:

            return Response(json.dumps("You can not send friend request now"), status=status.HTTP_400_BAD_REQUEST)

        if pending_friend_request is not None:

            return Response(json.dumps(f"Friend Request is already pending with {receiver_user.user.email}"), status=status.HTTP_400_BAD_REQUEST)

        serializer = PendingFriendRequestsSerializer(data=request.data, context={
            "request": request, "receiver_user": receiver_user
        })

        if serializer.is_valid():
            print("Done request")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Accept friend request of particular user
class AcceptFriendRequestView(generics.CreateAPIView):

    serializer_class = AcceptedFriendRequestsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Email will be the person whose request I want to accept
        email = request.data["email"].lower()
        sender = SocialProfile.objects.get(user__email__exact=email)
        receiver = SocialProfile.objects.get(user=request.user)
        pending = PendingFriendRequests.objects.filter(
            Q(sender=sender) & Q(receiver=receiver)).first()

        if pending is None:
            return Response(json.dumps("Friend Request doesn't exist in system"), status=status.HTTP_400_BAD_REQUEST
                            )

        serializer = AcceptedFriendRequestsSerializer(data=request.data, context={
            "sender": receiver, "receiver": sender
        })

        if serializer.is_valid():
            pending.delete()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequestView(generics.CreateAPIView):

    serializer_class = RejectedFriendRequestsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        email = request.data["email"].lower()
        sender = SocialProfile.objects.get(user__email__exact=email)
        receiver = SocialProfile.objects.get(user=request.user)
        pending = PendingFriendRequests.objects.filter(
            Q(sender=sender) & Q(receiver=receiver)).first()

        if pending is None:
            return Response(json.dumps("Friend Request doesn't exist in system"), status=status.HTTP_400_BAD_REQUEST)

        serializer = RejectedFriendRequestsSerializer(data=request.data, context={
            "sender": receiver, "receiver": sender
        })

        if serializer.is_valid():
            pending.delete()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListAcceptedFriendRequestsView(generics.ListAPIView):

    serializer_class = AcceptedFriendRequestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        social_user = SocialProfile.objects.get(user=self.request.user)

        accepted_friend_requests = AcceptdFriendRequests.objects.filter(
            sender=social_user)

        return accepted_friend_requests


class ListRejectedFriendRequestsView(generics.ListAPIView):

    serializer_class = RejectedFriendRequestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        social_user = SocialProfile.objects.get(user=self.request.user)

        rejected_friend_requests = RejectedFriendRequests.objects.filter(
            sender=social_user)

        return rejected_friend_requests


class ListPendingFriendRequestsView(generics.ListAPIView):

    serializer_class = PendingFriendRequestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        social_user = SocialProfile.objects.get(user=self.request.user)

        pending_friend_requests = PendingFriendRequests.objects.filter(
            receiver=social_user)

        return pending_friend_requests
