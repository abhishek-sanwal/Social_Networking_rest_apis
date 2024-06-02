from json import dumps

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

from .serializers import PendingFriendRequestsSerializer, \
    AcceptedFriendRequestsSerializer, RejectedFriendRequestsSerializer, \
    SocialProfileSerializer

from .models import SocialProfile, PendingFriendRequests, AcceptdFriendRequests, \
    RejectedFriendRequests

from .paginators import SmallResultsSetPagination
from .throttlers import SendApiThrottle

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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
        if "@" in search_word:
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


class SendFriendRequestView(CreateAPIView):

    serializer_class = PendingFriendRequestsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [SendApiThrottle]

    def post(self, request):

        print(request.data)
        email = request.data["email"].lower()
        print("email received")
        receiver_user = SocialProfile.objects.filter(
            user__email__exact=email).first()

        if receiver_user is None:

            return Response(json.loads({
                "text": "Provided email is not a valid user."
            }), status=status.HTTP_400_BAD_REQUEST)

        serializer = PendingFriendRequestsSerializer(data=request.data, context={
            "request": request, "receiver_user": receiver_user
        })

        if serializer.is_valid():
            print("Done request")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Accept friend request of particular user
class AcceptFriendRequestView(CreateAPIView):

    serializer_class = AcceptedFriendRequestsSerializer

    def post(self, request):

        email = request.data["email"].lower()
        sender = SocialProfile.objects.get(user=request.user)
        receiver = SocialProfile.objects.get(user__email__exact=email)
        pending = PendingFriendRequests.objects.filter(
            Q(sender=sender) | Q(receiver=receiver)).first()

        if pending is None:
            return Response(json.dumps({
                "text": "Friend Request doesn't exist in system, status = \
                    status.HTTP_400_BAD_REQUEST"
            }))

        serializer = AcceptedFriendRequestsSerializer(data=request.data, context={
            "sender": sender, "receiver": receiver
        })

        if serializer.is_valid():
            pending.delete()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequestView(CreateAPIView):

    serializer_class = RejectedFriendRequestsSerializer

    def post(self, request):

        email = request.data["email"].lower()
        sender = SocialProfile.objects.get(user=request.user)
        receiver = SocialProfile.objects.get(user__email__exact=email)
        pending = PendingFriendRequests.objects.filter(
            Q(sender=sender) | Q(receiver=receiver)).first()

        if pending is None:
            return Response(json.dumps({
                "text": "Friend Request doesn't exist in system, status = \
                    status.HTTP_400_BAD_REQUEST"
            }))

        serializer = RejectedFriendRequestsSerializer(data=request.data, context={
            "sender": sender, "receiver": receiver
        })

        if serializer.is_valid():
            pending.delete()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListAcceptedFriendRequestsView(generics.ListAPIView):

    serializer_class = AcceptedFriendRequestsSerializer

    def get_queryset(self):

        social_user = SocialProfile.objects.get(user=self.request.user)

        accepted_friend_requests = AcceptdFriendRequests.objects.filter(
            sender=social_user)

        return accepted_friend_requests


class ListRejectedFriendRequestsView(generics.ListAPIView):

    serializer_class = RejectedFriendRequestsSerializer

    def get_queryset(self):

        social_user = SocialProfile.objects.get(user=self.request.user)

        rejected_friend_requests = RejectedFriendRequests.objects.filter(
            sender=social_user)

        return rejected_friend_requests


class ListPendingFriendRequestsView(generics.ListAPIView):

    serializer_class = PendingFriendRequestsSerializer

    def get_queryset(self):

        social_user = SocialProfile.objects.get(user=self.request.user)

        pending_friend_requests = PendingFriendRequests.objects.filter(
            receiver=social_user)

        return pending_friend_requests
