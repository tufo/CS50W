from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request):
    if not request.user.is_authenticated: # tells us if user is signed in or not; if not...
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")
    
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"] # get the inputs
        password = request.POST["password"]

        # Now, try to authenticate this user.
        user = authenticate(request, username=username, password=password)
        if user is not None: # if successful...
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else: # if authentication failed...
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })
        
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out."
    })