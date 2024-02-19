from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from account.forms import LoginForm, SignupForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("blog:post_list"))
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd["password"])
            user.save()
            return redirect(reverse("account:login"))
    else:
        form = SignupForm()

    return render(request, "account/signup.html", {"form": form})
