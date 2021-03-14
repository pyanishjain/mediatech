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
        fields = ['ip_address', 'phoneNo', 'user']
        extra_kwargs = {
            'user':  {'read_only': True}
        }


class TelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram
        fields = ['DemoDate', 'licenceExpireDate', 'profile','isActive']


class WhatsappSerializer(serializers.ModelSerializer):
    class Meta:
        model = Whatsapp
        fields = ['DemoDate', 'licenceExpireDate', 'profile','isActive']


class InstagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instagram
        fields = ['DemoDate', 'licenceExpireDate', 'profile','isActive']
