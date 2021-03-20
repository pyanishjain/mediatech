from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phoneNo', 'user']
        extra_kwargs = {
            'user':  {'read_only': True}
        }


class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = ['whatsapp_class_xpath', ]


class TelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram
        fields = ['DemoDate', 'licenceExpireDate', 'profile', 'isActive','ip_address']


class WhatsappSerializer(serializers.ModelSerializer):
    class Meta:
        model = Whatsapp
        fields = ['DemoDate', 'licenceExpireDate', 'profile', 'isActive','ip_address']


class InstagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instagram
        fields = ['DemoDate', 'licenceExpireDate', 'profile', 'isActive','ip_address']
