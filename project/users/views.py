from django.shortcuts import render
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .serializers import RegisterSerializer
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class SignupApi(CreateAPIView):

    serializer_class = UserSerializer

    def post(self, request):

        serializer = UserSerializer(
            data=request.data, context={"request": request})

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LoginApi(CreateAPIView):

    serializer_class = UserSerializer()

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        email = request.data["email"]
        password = request.data["password"]
        user = authenticate(username=email, pasword=password)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@login_required
def home(request):

    return HttpResponse("<h3> Welcome bro</h3>")


def signup(request):

    form = SignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            form.save()
            email = form.cleaned_data["email"]
            messages.success(
                request, f"Hi, {email} You have been signed up to our website ")
            print("Signup Successful")
            return redirect('login')

        print("Signup Unsuccessful")
        messages.warning(request, "Some error occured. Please retry.")
        return redirect('signup')
    print("Signup process intiatied")
    return render(request, template_name="signup.html", context={
        "form": form
    })


def login(request):

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        email = form.cleaned_data["email"].lower()
        password = form.cleaned_data["password"]

        user = authenticate(username=email, password=password)

        if user is None:
            messages.warning(request, "No user exist with given email")
            return redirect('signup')

        login(request, user)
        messages.success(request, "You have been logged into successfully.")
        return redirect('home')

    return render(request, template_name="login.html", context={
        "form": form
    })
