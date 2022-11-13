from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
            messages.error(request, "ce nom d'utilisateur est deja utilisé")
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, "cette email a deja un compte")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "nom d'utilisateur incorrecte")
            return redirect('register')

        if password != password1:
            messages.error(request, "les deux mot de passe ne coincide pas")
            return redirect('register')
        
        my_user = User.objects.create_user(username,email,password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.save()
        messages.success(request, "Votre compte a était crée")
        return redirect('login')
        

    return render(request, 'account/register.html')

def log_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)     
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return redirect('home')
        else:
            messages.error(request,"Erreur d'authentification ...")
            return redirect('login')
    return render(request, 'account/login.html')

def log_out(request):
    logout(request)
    # messages.success(request, "Vous avez bien etait déconecté")
    return redirect('home')    
