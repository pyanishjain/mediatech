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


# @login_required(login_url='login')
def index(request):
    token = ''
    try:
        user = request.user
        token = Token.objects.filter(user=user).first()
    except Exception as e:
        print('!!!!!!!!!!!!!!!!!!!!', e)
    print("$$$$$$$$$$$$$$$$$$$$$$", token)
    return render(request, 'main.html', {'token': token})


def signup(request):
    try:
        if request.user.reseller.token_count <= 0:
            return HttpResponse('Please Buy Tokens!!')
    except:
        pass

    signup_form = SignUpForm()
    profile_form = UserProfileForm()

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():

            user = signup_form.save()
            # Create Token
            token, created = Token.objects.get_or_create(user=user)
            # print(token)

            profile = profile_form.save(commit=False)
            profile.token = token
            profile.user = user
            profile.unhash_password = request.POST.get('password1')
            if not request.user.is_anonymous:
                print(request.user)
                profile.reseller = request.user.reseller
                profile.save()
                return redirect('dashboard')
            else:
                profile.save()
                print("Not reseller")
                user = authenticate(username=request.POST.get(
                    'username'), password=request.POST.get('password1'))
                login(request, user)
                return redirect('index')

    context = {'signup_form': signup_form, 'profile_form': profile_form}
    return render(request, 'registration/signup.html', context)


def dashboard(request):
    profile = Profile.objects.filter(reseller=request.user.reseller)
    # user_list = [p.user for p in profile ]
    # tokens =  Token.objects.filter(user__in=user_list)
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$!#@!@#!#$!',tokens)

    # tokens = Token.objects.filter(user=request.user)
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print(profile[0].token)

    # print('##$!#@$!#@$!#@$!#@$!@#$!#@$@!#', type(request.user.reseller))

    telegram = Telegram.objects.filter(reseller=request.user.reseller)
    whatsapp = Whatsapp.objects.filter(reseller=request.user.reseller)
    instagram = Instagram.objects.filter(reseller=request.user.reseller)

    context = {'profile': profile, 'telegrams': telegram,
               'whatsapps': whatsapp, 'instagrams': instagram}
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
        reseller = request.user.profile.reseller
        db, created = Telegram.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)
        if created:
            db.DemoDate = datetime.today()
            db.save()
            profile = Telegram.objects.filter(
                profile=request.user.profile).first()
    serializers = TelegramSerializer(instance=profile)
    return Response(serializers.data)


@api_view(['GET'])
def instagramAPI(request):
    profile = Instagram.objects.filter(profile=request.user.profile).first()
    if profile == None:
        reseller = request.user.profile.reseller
        db, created = Instagram.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)
        if created:
            db.DemoDate = datetime.today()
            db.save()
            profile = Instagram.objects.filter(
                profile=request.user.profile).first()
    serializers = InstagramSerializer(instance=profile)
    return Response(serializers.data)


@api_view(['GET'])
def whatsappAPI(request):
    profile = Whatsapp.objects.filter(profile=request.user.profile).first()
    if profile == None:
        reseller = request.user.profile.reseller
        db, created = Whatsapp.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)
        print(created)
        if created:
            db.DemoDate = datetime.today()
            db.save()
            profile = Whatsapp.objects.filter(
                profile=request.user.profile).first()

    serializers = WhatsappSerializer(instance=profile)
    return Response(serializers.data)


def update(request, id, api):
    if api == 'telegram':
        telegram = Telegram.objects.filter(reseller=request.user.reseller)
        profile = telegram.get(id=id)
        form = TelegramForm(instance=profile, isPaid_check=profile.isPaid)

    if api == 'whatsapp':
        whatsapp = Whatsapp.objects.filter(reseller=request.user.reseller)
        profile = whatsapp.get(id=id)
        form = WhatsappForm(instance=profile, isPaid_check=profile.isPaid)

    if api == 'instagram':
        instagram = Instagram.objects.filter(reseller=request.user.reseller)
        profile = telegram.get(id=id)
        form = InstagramForm(instance=profile, isPaid_check=profile.isPaid)

    if request.method == 'POST':
        if api == 'telegram':
            form = TelegramForm(request.POST, instance=profile,
                                isPaid_check=profile.isPaid)
        if api == 'whatsapp':
            form = WhatsappForm(request.POST, instance=profile,
                                isPaid_check=profile.isPaid)
        if api == 'instagram':
            form = InstagramForm(request.POST, instance=profile,
                                 isPaid_check=profile.isPaid)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print("Some error")
            return render(request, 'update_telegram.html', {'form': form})

    return render(request, 'update_telegram.html', {'form': form})


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


def plan_detail(request):
    plans = Plan.objects.all()
    return render(request, 'plan_detail.html', {'plans': plans})


def contact(request):
    try:
        if request.user.profile.reseller:
            print(type(request.user.profile.reseller))

            contacts = Reseller.objects.filter(
                reseller=request.user.profile.reseller.reseller)
            return render(request, 'contact.html', {'contacts': contacts})
    except Exception as e:
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', e)

    contacts = Contact.objects.all()
    return render(request, 'contact.html', {'contacts': contacts})


@csrf_exempt
def updateSoftware(request):
    data = json.loads(request.body)
    print('#################################################3', data)
    plan_id = int(data['plan'])
    reseller = request.user.profile.reseller
    software_name = data['software_name']
    if software_name == 'telegram':
        db, created = Telegram.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)

    if software_name == 'instagram':
        db, created = Instagram.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)

    if software_name == 'whatsapp':
        db, created = Whatsapp.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)

    plan = Plan.objects.get(pk=plan_id)
    duration = plan.duration

    if created:
        db.duration = int(duration)
        db.plan = plan
        db.isDemo = True
        db.DemoDate = datetime.today()
    db.save()
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


# APIS
@api_view(['GET'])
def serverDateAPI(request):
    today = datetime.today().date()
    return Response(today)


@api_view(['PUT'])
def isPaidStatus(request, api):
    today = datetime.today().date()
    if api == 'telegram':
        obj = Telegram.objects.get(profile=request.user.profile)
    if api == 'whatsapp':
        obj = Whatsapp.objects.get(profile=request.user.profile)
    if api == 'instagram':
        obj = Instagram.objects.get(profile=request.user.profile)
    if today > obj.licenceExpireDate:
        obj.isPaid = False
        obj.licenceExpireDate = None
        obj.save()

    return Response('ok')


@api_view(['GET'])
def IpAPI(request, api):
    if api == 'whatsapp':
        ips = Whatsapp.objects.values_list(
            'ip_address').exclude(ip_address=None)
    if api == 'telegram':
        ips = Telegram.objects.values_list(
            'ip_address').exclude(ip_address=None)
    if api == 'instagram':
        ips = Instagram.objects.values_list(
            'ip_address').exclude(ip_address=None)
    return Response(ips)


@api_view(['PUT'])
def createIP(request, api):
    if api == 'whatsapp':
        profile = Whatsapp.objects.filter(profile=request.user.profile).first()
        serializer = WhatsappSerializer(instance=profile, data=request.data)
    if api == 'telegram':
        profile = Telegram.objects.filter(profile=request.user.profile).first()
        serializer = TelegramSerializer(instance=profile, data=request.data)
    if api == 'instagram':
        profile = Instagram.objects.filter(
            profile=request.user.profile).first()
        serializer = InstagramSerializer(instance=profile, data=request.data)

    if serializer.is_valid():
        print(serializer)
        ip = serializer.save()
        ip.ip_address = request.data['ip_address']
        ip.save()
    else:
        return Response("Please check Your Token")
    return Response('hi')


@api_view(['GET'])
def variableAPI(request, api):
    if api == 'whatsapp':
        variable = Software.objects.values_list('whatsapp_class_xpath')
    if api == 'telegram':
        variable = Software.objects.values_list('telegram_class_xpath')

    return Response(variable)
