from django.shortcuts import render

from .serializers import PendingFriendRequestsSerializer, \
    AcceptedFriendRequestsSerializer, RejectedFriendRequestsSerializer, SocialProfileSerializer

# Create your views here.
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import generics

from .models import SocialProfile

from rest_framework.response import Response
from rest_framework import status


class UserSearchApi(APIView):

    def get(self, request):

        search_word = request.data["search_word"]
        print(search_word)
        # If search_word is a email
        if "@" in search_word:

            social_user = SocialProfile.objects.filter(
                user__email__exact=search_word)

            if not social_user:
                social_user = SocialProfile.objects.filter(
                    user__email__contains=search_word)

            serializer = SocialProfileSerializer(social_user, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Else search_word is a user
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


class SendFriendRequest(CreateAPIView):

    serializer_class = PendingFriendRequestsSerializer


class AcceptFriendRequest(CreateAPIView):

    serializer_class = AcceptedFriendRequestsSerializer


class RejectFriendRequest(CreateAPIView):

    serializer_class = RejectedFriendRequestsSerializer
