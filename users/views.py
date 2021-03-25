from django.db.models import F
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

from django.http import HttpResponse
import csv


@login_required(login_url='login')
def exportToCSV(request, api):
    table = json.loads(request.COOKIES['mycookie'])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{api}.csv"'
    writer = csv.writer(response)
    for t in table:
        writer.writerow(t)
    return response


# @login_required(login_url='login')
def index(request):
    token = ''
    try:
        user = request.user
        token = Token.objects.filter(user=user).first()
    except Exception as e:
        pass
    telegram_url = Software.objects.all().first().telegram.url
    whatsapp_url = Software.objects.all().first().whatsapp.url
    instagram_url = Software.objects.all().first().instagram.url
    return render(request, 'main.html', {'token': token, 'telegram_url': telegram_url, 'whatsapp_url': whatsapp_url, 'instagram_url': instagram_url})


def signup(request):
    try:
        if request.user.reseller.token_count <= 0:
            return HttpResponse('<h1 style="text-align:center;">Your Have 0 Token LEFT  Please Contact </h1')
        if not request.user.reseller.isActive:
            return HttpResponse('<h1 style="text-align:center;">Your Account Is Deactive Please Contact </h1')
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

            profile = profile_form.save(commit=False)
            profile.token = token
            profile.user = user
            profile.unhash_password = request.POST.get('password1')
            if not request.user.is_anonymous:
                profile.reseller = request.user.reseller
                profile.save()
                return redirect('dashboard')
            else:
                profile.save()
                user = authenticate(username=request.POST.get(
                    'username'), password=request.POST.get('password1'))
                login(request, user)
                return redirect('index')

    context = {'signup_form': signup_form, 'profile_form': profile_form}
    return render(request, 'registration/signup.html', context)


def dashboard(request):
    reseller_form = ''
    if request.user.is_staff:
        profile = Profile.objects.all()
        telegram = Telegram.objects.all()
        whatsapp = Whatsapp.objects.all()
        instagram = Instagram.objects.all()
        reseller_form = ResellerForm()

    else:
        profile = Profile.objects.filter(reseller=request.user.reseller)
        telegram = Telegram.objects.filter(reseller=request.user.reseller)
        whatsapp = Whatsapp.objects.filter(reseller=request.user.reseller)
        instagram = Instagram.objects.filter(reseller=request.user.reseller)

    context = {'profile': profile, 'telegrams': telegram,
               'whatsapps': whatsapp, 'instagrams': instagram, 'reseller_form': reseller_form}
    return render(request, 'dashboard.html', context)


def filterDashboard(request, api):
    today = datetime.today().date()
    if request.user.is_staff:
        if api == 'profile':
            theObject = Profile.objects.all()
        if api == 'telegram':
            theObject = Telegram.objects.all()
        if api == 'whatsapp':
            theObject = Whatsapp.objects.all()
        if api == 'instagram':
            theObject = Instagram.objects.all()
    else:
        if api == 'telegram':
            theObject = Telegram.objects.filter(reseller=request.user.reseller)
        if api == 'whatsapp':
            theObject = Whatsapp.objects.filter(reseller=request.user.reseller)
        if api == 'instagram':
            theObject = Instagram.objects.filter(
                reseller=request.user.reseller)

    if request.user.is_staff:
        if not request.GET.get('reseller') == '':
            theObject = theObject.filter(reseller=request.GET.get('reseller'))
    else:
        if not request.GET.get('reseller') == None:
            theObject = theObject.filter(reseller=request.GET.get('reseller'))
    try:
        if not request.GET.get('Paid') == None:
            if request.GET.get('Paid') == 'isPaid':
                theObject = theObject.filter(isPaid=True)
            if request.GET.get('Paid') == 'isNotPaid':
                theObject = theObject.filter(isPaid=False)
    except:
        pass
    try:
        if not request.GET.get('Active') == None:
            if request.GET.get('Active') == 'isActive':
                theObject = theObject.filter(isActive=True)
            if request.GET.get('Active') == 'isNotActive':
                theObject = theObject.filter(isActive=False)
    except:
        pass

    if not request.GET.get('lessThenMonth') == None:
        IDs = []
        for o in theObject:
            try:
                if (o.licenceExpireDate - today).days <= 31:
                    IDs.append(o.id)
            except Exception as e:
                pass
        if len(IDs) > 0:
            theObject = theObject.filter(id__in=IDs)
    try:
        if not request.GET.get('todayDemo') == None:
            theObject = theObject.filter(DemoDate=today)
    except:
        pass

    return render(request, 'filter_dashboard.html', {'theObject': theObject})


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
def whatsappAPI(request):
    profile = Whatsapp.objects.filter(profile=request.user.profile).first()
    if profile == None:
        reseller = request.user.profile.reseller
        db, created = Whatsapp.objects.get_or_create(
            profile=request.user.profile, reseller=reseller)
        if created:
            db.DemoDate = datetime.today()
            db.save()
            profile = Whatsapp.objects.filter(
                profile=request.user.profile).first()

    serializers = WhatsappSerializer(instance=profile)
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


# Updates the User INFO
def update(request, id, api):
    if request.user.is_staff:
        if api == 'telegram':
            telegram = Telegram.objects.all()
            profile = telegram.get(id=id)
            form = TelegramForm(instance=profile, isPaid_check=profile.isPaid)

        if api == 'whatsapp':
            whatsapp = Whatsapp.objects.all()
            profile = whatsapp.get(id=id)
            form = WhatsappForm(instance=profile, isPaid_check=profile.isPaid)

        if api == 'instagram':
            instagram = Instagram.objects.all()
            profile = instagram.get(id=id)
            form = InstagramForm(instance=profile, isPaid_check=profile.isPaid)

    else:
        if api == 'telegram':
            telegram = Telegram.objects.filter(reseller=request.user.reseller)
            profile = telegram.get(id=id)
            form = TelegramForm(instance=profile, isPaid_check=profile.isPaid)

        if api == 'whatsapp':
            whatsapp = Whatsapp.objects.filter(reseller=request.user.reseller)
            profile = whatsapp.get(id=id)
            form = WhatsappForm(instance=profile, isPaid_check=profile.isPaid)

        if api == 'instagram':
            instagram = Instagram.objects.filter(
                reseller=request.user.reseller)
            profile = instagram.get(id=id)
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
            return render(request, 'update_telegram.html', {'form': form})

    return render(request, 'update_telegram.html', {'form': form})


def contact(request):
    try:
        if request.user.profile.reseller:
            contacts = Reseller.objects.filter(
                reseller=request.user.profile.reseller.reseller)
            return render(request, 'contact.html', {'contacts': contacts})
    except Exception as e:
        pass
    contacts = Contact.objects.all()
    return render(request, 'contact.html', {'contacts': contacts})


# APIS FOR DESKTOP SOFTWARE
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


# class profileList(generics.ListAPIView):
#     serializer_class = ProfileSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Profile.objects.filter(user=user)


# @api_view(['PUT'])
# def updateWithTokenProfile(request):
#     profile = Profile.objects.filter(user=request.user).first()
#     lc = profile.locationCount
#     kc = profile.keywordCount

#     serializer = ProfileSerializer(instance=profile, data=request.data)
#     if serializer.is_valid():
#         update = serializer.save()
#         update.locationCount = lc+request.data['locationCount']

#         update.save()
#     else:
#         return Response("something went wring!!!")
#     return Response("Updated sucessfully!!")

# def downloadSoftware(request, name):
#     if name == 'telegram':
#         software_url = Software.objects.all().first().telegram.url

#     if name == 'instagram':
#         software_url = Software.objects.all().first().instagram.url


#     if name == 'whatsapp':
#         software_url = Software.objects.all().first().whatsapp.url

#     plan_form = PlanForm()
#     context = {'plan_form': plan_form,
#                'software_url': software_url, 'software_name': name}
#     return render(request, 'registration/software.html', context)


# def plan_detail(request):
#     plans = Plan.objects.all()
#     return render(request, 'plan_detail.html', {'plans': plans})


# @csrf_exempt
# def updateSoftware(request):
#     data = json.loads(request.body)
#     plan_id = int(data['plan'])
#     reseller = request.user.profile.reseller
#     software_name = data['software_name']
#     if software_name == 'telegram':
#         db, created = Telegram.objects.get_or_create(
#             profile=request.user.profile, reseller=reseller)

#     if software_name == 'instagram':
#         db, created = Instagram.objects.get_or_create(
#             profile=request.user.profile, reseller=reseller)

#     if software_name == 'whatsapp':
#         db, created = Whatsapp.objects.get_or_create(
#             profile=request.user.profile, reseller=reseller)

#     plan = Plan.objects.get(pk=plan_id)
#     duration = plan.duration

#     if created:
#         db.duration = int(duration)
#         db.plan = plan
#         db.isDemo = True
#         db.DemoDate = datetime.today()
#     db.save()
#     return JsonResponse("Hi there!", safe=False)


# Accounts

# def login_user(request):
#     if request.method == 'POST':
#         User_Form = UserForm(request.POST)
#         user = authenticate(username=request.POST.get(
#             'username'), password=request.POST.get('password'))
#         if user:
#             login(request, user)
#             isReseller = user.profile.isReseller
#             if isReseller:
#                 return redirect('signup')
#             else:
#                 pass
#             return redirect("index")
#         else:
#             context = {'form': UserForm(request.POST)}
#             # messages.error(
#             #     request, " Login Failed! Please check your username and password")
#             return render(request, 'registration/login.html', context)

#     else:
#         context = {'form': UserForm()}
#         return render(request, 'registration/login.html', context)
