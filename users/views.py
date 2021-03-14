from http.client import responses
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from .forms import *
import dateutil.relativedelta as delta
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import *
from django.contrib.auth.decorators import login_required
import socket
import json
from django.http import JsonResponse
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login')
def index(request):
    user = request.user
    token = Token.objects.filter(user=user).first()
    return render(request, 'main.html', {'token': token})


def signup(request):
    signup_form = SignUpForm()
    profile_form = UserProfileForm()

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',
        #       request.POST.get('password1'))
        # return HttpResponse("Hi")
        profile_form = UserProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save()
            # Create Token
            Token.objects.create(user=user)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.unhash_password = request.POST.get('password1')
            if not request.user.is_anonymous:
                print(request.user)
                profile.reseller = request.user.reseller
            else:
                print("Not reseller")
            profile.save()

    context = {'signup_form': signup_form, 'profile_form': profile_form}
    return render(request, 'registration/signup.html', context)


def dashboard(request):
    profile = Profile.objects.filter(reseller=request.user.reseller)
    telegram = Telegram.objects.filter(reseller=request.user.reseller)
    whatsapp = Whatsapp.objects.filter(reseller=request.user.reseller)
    instagram = Instagram.objects.filter(reseller=request.user.reseller)

    print("#######################", telegram)

    # print(telegram)
    context = {'profile': profile, 'telegrams': telegram}
    return render(request, 'dashboard.html', context)


class profileList(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)


@api_view(['PUT'])
def updateWithTokenProfile(request):
    profile = Profile.objects.filter(user=request.user).first()
    # body_lc = request.data['locationCount']
    # body_kc = request.data['keywordCount']
    lc = profile.locationCount
    kc = profile.keywordCount

    serializer = ProfileSerializer(instance=profile, data=request.data)
    if serializer.is_valid():
        print("!!!!!!!!!!!!!!!!", profile.locationCount, profile.locationCount)
        update = serializer.save()
        update.locationCount = lc+request.data['locationCount']

        update.save()
    else:
        return Response("something went wring!!!")
    return Response("Updated sucessfully!!")


@api_view(['GET'])
def telegramAPI(request):
    profile = Telegram.objects.filter(profile=request.user.profile).first()
    if profile == None:
        return Response("Please check your token")
    serializers = TelegramSerializer(instance=profile)
    return Response(serializers.data)


@api_view(['GET'])
def instagramAPI(request):
    profile = Instagram.objects.filter(profile=request.user.profile).first()
    if profile == None:
        return Response(status=responses.status.HTTP_201_CREATED)
    serializers = InstagramSerializer(instance=profile)
    return Response(serializers.data)


@api_view(['GET'])
def whatsappAPI(request):
    profile = Whatsapp.objects.filter(profile=request.user.profile).first()
    if profile == None:
        return Response(False)
    serializers = WhatsappSerializer(instance=profile)
    return Response(serializers.data)


@api_view(['PUT'])
def UpdateUserIp(request):
    profile = Profile.objects.filter(user=request.user).first()
    serializer = ProfileSerializer(instance=profile, data=request.data)
    if serializer.is_valid():
        ip = serializer.save()
        ip.ip_address = request.data['ip_address']
        ip.save()
    else:
        return Response("Please check Your Token")
    return Response("Update Sucessfully!")


def downloadSoftware(request, name):
    if name == 'telegram':
        software_url = Software.objects.all().first().telegram.url
        print(software_url)

    if name == 'instagram':
        software_url = Software.objects.all().first().instagram.url
        print(software_url)

    if name == 'whatsapp':
        software_url = Software.objects.all().first().whatsapp.url
        print(software_url)

    plan_form = PlanForm()
    context = {'plan_form': plan_form,
               'software_url': software_url, 'software_name': name}
    return render(request, 'registration/software.html', context)


@csrf_exempt
def updateSoftware(request):
    data = json.loads(request.body)
    print(data)
    plan_id = int(data['plan'])
    reseller = data['reseller']

    # reseller_profile = User.objects.get(id=int(reseller))

    # print("FADSFADSFADSFADSFADSFADSFADSFADSF", reseller_profile)

    # print("#%#$%#$%$%^$%^%^$%$%#$%#$%", reseller)

    reseller = request.user.profile.reseller
    print("################################", reseller)

    software_name = data['software_name']
    if software_name == 'telegram':
        db, created = Telegram.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)

    if software_name == 'instagram':
        db, created = Instagram.objects.get_or_create(
            profile=request.user.profile, reseller=reseller_profile)

    if software_name == 'whatsapp':
        db, created = Whatsapp.objects.get_or_create(
            profile=request.user.profile, reseller=reseller_profile)

    print(db)
    print(created)

    # print("DATABASE$$$$$$$$$$$$$$$$$$$$$$$$$$$", db.duration)

    # print(db)
    # if created:
    plan = Plan.objects.get(pk=plan_id)
    duration = plan.duration

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", duration, type(duration))

    # db.licenceExpireDate = request.user.date_joined + \
    #     delta.relativedelta(months=int(duration))

    db.isDemo = True
    # db.duration = int(duration)
    db.plan = plan
    if created:
        db.DemoDate = datetime.today()

    # db.locationCount = plan.locationCount
    # db.keywordCount = plan.keywordCount
    print('####################################', db.date_updated)
    db.save()

    print(plan)
    return JsonResponse("Hi there!", safe=False)


# Accounts

def login_user(request):
    if request.method == 'POST':
        User_Form = UserForm(request.POST)
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            isReseller = user.profile.isReseller
            if isReseller:
                return redirect('signup')
            else:
                pass
            return redirect("index")
        else:
            context = {'form': UserForm(request.POST)}
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # messages.error(
            #     request, " Login Failed! Please check your username and password")
            return render(request, 'registration/login.html', context)

    else:
        context = {'form': UserForm()}
        return render(request, 'registration/login.html', context)


def updateTelegram(request, id):
    telegram = Telegram.objects.filter(reseller=request.user.reseller)
    tel_profile = telegram.get(id=id)
    form = TelegramForm(instance=tel_profile)

    if request.method == 'POST':
        form = TelegramForm(request.POST, instance=tel_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print("Some error")
            return render(request, 'update_telegram.html', {'form': form})

    return render(request, 'update_telegram.html', {'form': form})




# APIS
@api_view(['GET'])
def serverDateAPI(request):
    today = datetime.today().date()
    return Response(today)


@api_view(['GET'])
def IpAPI(request):
    ips = Profile.objects.values_list('ip_address').exclude(ip_address=None)
    return Response(ips)
