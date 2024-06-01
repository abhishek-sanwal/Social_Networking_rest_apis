from django.shortcuts import render

from .serializers import PendingFriendRequestsSerializer, \
    AcceptedFriendRequestsSerializer, RejectedFriendRequestsSerializer, \
    SocialProfileSerializer

# Create your views here.
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import generics

from .models import SocialProfile

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import json


class UserSearchApi(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        #  IF search word is not provided
        if "search_word" not in request.data:
            data = " Either email or username is required to search"
            return Response(json.dumps(data), status=status.HTTP_400_BAD_REQUEST)

        search_word = request.data["search_word"]
        # print(search_word)
        # If search_word is a email
        if "@" in search_word:
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


class SendFriendRequest(CreateAPIView):

    serializer_class = PendingFriendRequestsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        print(request.data)
        email = request.data["email"]
        print("email received")
        receiver_user = SocialProfile.objects.filter(
            user__email__exact=email).first()

        if receiver_user is None:

            return Response(json.loads({
                "Provided email is not a valid user."
            }), status=status.HTTP_400_BAD_REQUEST)

        serializer = PendingFriendRequestsSerializer(data=request.data, context={
            "request": request, "receiver_user": receiver_user
        })

        if serializer.is_valid():
            print("Done request")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequest(CreateAPIView):

    serializer_class = AcceptedFriendRequestsSerializer
    pass


class RejectFriendRequest(CreateAPIView):

    serializer_class = RejectedFriendRequestsSerializer

    def post(self, request):

        pass
