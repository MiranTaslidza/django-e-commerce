from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login

#login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # koristi Django login
            return redirect('home')
        else:
            # možeš dodati poruku da su loši podaci
            pass
    return render(request, 'profiles/login.html')


#logout
def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, "profiles/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
    return render(request, "profiles/register.html", {"form": form})
