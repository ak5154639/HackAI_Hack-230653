from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
import requests
from django.db import IntegrityError

from decouple import config

import json

from django.contrib.auth.models import User

from .models import tempData


# Create your views here.
def index(request):
    temperatureData = None
    if request.user.is_authenticated:
        
        temperatureData = tempData.objects.get(user=request.user)

        result = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config('WEATHER_API_KEY')}&q={temperatureData.city}")
        result = result.json()
        # print(result["current"]["temp_c"])
        temperatureData.current_temperature = result["current"]["temp_c"]
        temperatureData.local_time = result["location"]["localtime"]

    return render(request, "TemperatureAlert/index.html", {
        "data":temperatureData
    })

def signup(request):
    if request.method == 'POST':
        name = request.POST["name"]
        username = request.POST["userid"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        if password != confirm_password:
            return render(request, "TemperatureAlert/signup.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = name
            user.save()

            temperatureData = tempData(user=user)
            temperatureData.save()
        except IntegrityError:
            return render(request, "TemperatureAlert/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "TemperatureAlert/signup.html")


def login_view(request):
    if request.method == 'POST':
        # Attempt to sign user in
        userid = request.POST["userid"]
        password = request.POST["password"]
        user = authenticate(request, username=userid, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "TemperatureAlert/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "TemperatureAlert/login.html")

def changeCity(request):
    if request.method == 'POST':
        city = request.POST["city"]
        lower_temperature = request.POST["lower_temperature"]
        upper_temperature = request.POST["upper_temperature"]

        if lower_temperature > upper_temperature:
            return render(request, "TemperatureAlert/changeCity.html", {
                "data": tempData.objects.get(user=request.user),
                "message": "Lower bound should be less than the upper bound."
            })
        
        result = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config('WEATHER_API_KEY')}&q={city}")

        if not result.ok:
            return render(request, "TemperatureAlert/changeCity.html", {
                "message": "Invalid City Name",
                "data": tempData.objects.get(user=request.user)
            })

        try:
            temperatureData = tempData.objects.get(user=request.user)
            temperatureData.city = city
            temperatureData.lower_temperature = lower_temperature
            temperatureData.upper_temperature = upper_temperature

            temperatureData.save()

            # 

            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "TemperatureAlert/changeCity.html", {
                "data": tempData.objects.get(user=request.user),
                "message": "Some Error Occured"
            })
    else:
        return render(request, "TemperatureAlert/changeCity.html", {
            "data": tempData.objects.get(user=request.user)
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))