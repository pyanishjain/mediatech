from django.contrib import admin
from .models import *


class ResellerAdmin(admin.ModelAdmin):
    # search_fields = ['reseller', 'phoneNo', 'sold_token']

    list_filter = ['token_count', 'sold_token', 'isActive']

    list_display = ['reseller', 'token_count',
                    'sold_token', 'isActive', 'phoneNo']


class ProfileAdmin(admin.ModelAdmin):
    # search_fields=['user','phoneNo','token']

    list_filter = ['reseller']

    list_display = ['user', 'phoneNo', 'token', 'reseller']


class InstagramAdmin(admin.ModelAdmin):

    # search_fields = ['profile', 'reseller',
    #                  'DemoDate', 'licenceExpireDate', 'isPaid']

    list_filter = ['reseller', 'licenceExpireDate', 'DemoDate', 'isPaid']

    list_display = ['profile', 'reseller', 'licenceExpireDate', 'isPaid']


class WhatsappAdmin(admin.ModelAdmin):

    # search_fields=['profile','reseller','DemoDate','licenceExpireDate','isPaid']

    list_filter = ['reseller', 'licenceExpireDate', 'DemoDate', 'isPaid']

    list_display = ['profile', 'reseller', 'licenceExpireDate', 'isPaid']


class TelegramAdmin(admin.ModelAdmin):

    # search_fields=['profile','reseller','DemoDate','licenceExpireDate','isPaid']

    list_filter = ['reseller', 'licenceExpireDate', 'DemoDate', 'isPaid']

    list_display = ['profile', 'reseller', 'licenceExpireDate', 'isPaid']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Reseller, ResellerAdmin)
admin.site.register(Plan)
admin.site.register(Software)
admin.site.register(Telegram, TelegramAdmin)
admin.site.register(Whatsapp, WhatsappAdmin)
admin.site.register(Instagram, InstagramAdmin)
admin.site.register(Contact)
