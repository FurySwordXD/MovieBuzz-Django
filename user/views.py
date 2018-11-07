from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({"flag": True, "username": user.username, "email": user.email, "name": user.first_name + ' ' + user.last_name})
    return JsonResponse({"flag": False})

def sign_out(request):
    logout(request)
    return JsonResponse({"flag": True})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.first_name = name.split()[0]
        if len(name.split()) == 2:
            user.last_name = name.split()[1]
        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({"flag":True, "username": username, "email": email, "name": user.first_name + ' ' + user.last_name})

    return JsonResponse({"flag":False})

def edit_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        
        user = User.objects.get(username=username)
        user.email = email
        if password != '':
            user.set_password(password)
        user.first_name = name.split()[0]
        if name.split()[1]:
            user.last_name = name.split()[1]
        user.save()
        return JsonResponse({"flag":True, "username": username, "email": email, "name": name})

    return JsonResponse({"flag":False})
        

