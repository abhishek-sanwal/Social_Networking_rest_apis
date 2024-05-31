from django.shortcuts import render
from django.contrib import messages
from .forms import SignupForm, LoginForm
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


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
