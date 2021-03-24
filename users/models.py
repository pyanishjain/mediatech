from django.db import models
from django.contrib.auth.models import User
import dateutil.relativedelta as delta


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import datetime
from rest_framework.authtoken.models import Token


class Plan(models.Model):
    plan_name = models.CharField(max_length=256, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True, help_text='plan price')
    duration = models.IntegerField(null=True, help_text='Enter Months')
    locationCount = models.IntegerField(null=True, blank=True)
    keywordCount = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.plan_name)


class Software(models.Model):
    telegram = models.FileField(upload_to='software', null=True, blank=True)
    whatsapp = models.FileField(upload_to='software', null=True, blank=True)
    instagram = models.FileField(upload_to='software', null=True, blank=True)
    whatsapp_class_xpath = models.TextField(null=True, blank=True)
    telegram_class_xpath = models.TextField(null=True, blank=True)


class Contact(models.Model):
    phoneNo = models.IntegerField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.phoneNo)


class Reseller(models.Model):
    reseller = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    token_count = models.IntegerField(default=10)
    sold_token = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    phoneNo = models.CharField(null=True, max_length=10, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.reseller.__str__()


class Profile(models.Model):
    token = models.OneToOneField(
        Token, on_delete=models.CASCADE, null=True, blank=True)
    reseller = models.ForeignKey(
        Reseller, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phoneNo = models.CharField(null=True, max_length=10, blank=True)
    unhash_password = models.CharField(null=True, blank=True, max_length=256)

    def __str__(self):
        return self.user.__str__()


# class NoticeBoard(models.Model):
#     notice = models.TextField(null=True,blank=True)
#     def __str__(self):
#         return self.notice


class Base(models.Model):
    def createLicenceExpireDate(self):
        duration = self.duration
        x = self.date_updated + delta.relativedelta(months=int(duration))
        return x

    def save(self, *args, **kwargs):

        if self.isPaid == True and self.licenceExpireDate == None:
            self.licenceExpireDate = self.createLicenceExpireDate()
            try:
                self.reseller.token_count -= 1
                self.reseller.sold_token += 1
            except:
                pass

        # if self.licenceExpireDate < today:
        #     print("this time isPaid gona be False",self.isPaid)
        #     self.isPaid = False

        # if self.licenceExpireDate < today:
        #             print("this time isPaid gona be False",self.isPaid)
        #             self.isPaid = False

        # if self.isPaid:
            # try:
            #     # self.licenceExpireDate.date()
            #     if self.licenceExpireDate.date() < today:
            #         print("this time isPaid gona be False",self.isPaid)
            #         self.isPaid = False
            # except:
            #     # self.licenceExpireDate
            #     if self.licenceExpireDate < today:
            #         print("this time isPaid gona be False",self.isPaid)
            #         self.isPaid = False

        #     if not self.confirm_paid:
        #         self.licenceExpireDate = self.createLicenceExpireDate()
        #         try:
        #             self.reseller.token_count -= 1
        #             self.reseller.sold_token += 1
        #         except:
        #             pass
        #         self.confirm_paid = True
        # else:
        #     self.licenceExpireDate = self.DemoDate
        super().save(*args, **kwargs)


def save_reseller_token_count(sender, instance, **kwargs):
    if instance.reseller != None:
        instance.reseller.save()
    # else:
    #     instance.profile.save()


# def get_plan():
#     return Plan.objects.get(id=1)


class Telegram(Base):
    reseller = models.ForeignKey(
        Reseller, null=True, blank=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    # plan = models.ForeignKey(
    #     Plan, on_delete=models.CASCADE, null=True, blank=True, default=get_plan)

    duration = models.IntegerField(default=12)

    DemoDate = models.DateField(null=True, blank=True, default=timezone.now)
    licenceExpireDate = models.DateField(null=True, blank=True)
    isPaid = models.BooleanField(
        default=False, blank=True, help_text='only click when amount is paid')
    confirm_paid = models.BooleanField(
        default=False, help_text='do not fill this field')
    isActive = models.BooleanField(default=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(
        null=True, blank=True, max_length=256, help_text='do not fill this field')

    def __str__(self):
        return str(self.profile)


post_save.connect(save_reseller_token_count, sender=Telegram)


class Whatsapp(Base):
    reseller = models.ForeignKey(
        Reseller, null=True, blank=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    # plan = models.ForeignKey(
    #     Plan, on_delete=models.CASCADE, null=True, blank=True,default=get_plan)

    duration = models.IntegerField(default=12)

    DemoDate = models.DateField(null=True, blank=True, default=timezone.now)
    licenceExpireDate = models.DateField(null=True, blank=True)
    isPaid = models.BooleanField(
        default=False, blank=True, help_text='only click when amount is paid')
    confirm_paid = models.BooleanField(
        default=False, help_text='do not fill this field')
    isActive = models.BooleanField(default=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(
        null=True, blank=True, max_length=256, help_text='do not fill this field')

    def __str__(self):
        return str(self.profile)


post_save.connect(save_reseller_token_count, sender=Whatsapp)


class Instagram(Base):
    reseller = models.ForeignKey(
        Reseller, null=True, blank=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    # plan = models.ForeignKey(
    #     Plan, on_delete=models.CASCADE, null=True, blank=True,default=get_plan)

    duration = models.IntegerField(default=12)

    DemoDate = models.DateField(null=True, blank=True, default=timezone.now)
    licenceExpireDate = models.DateField(null=True, blank=True)
    isPaid = models.BooleanField(
        default=False, blank=True, help_text='only click when amount is paid')
    confirm_paid = models.BooleanField(
        default=False, help_text='do not fill this field')
    isActive = models.BooleanField(default=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(
        null=True, blank=True, max_length=256, help_text='do not fill this field')

    def __str__(self):
        return str(self.profile)


post_save.connect(save_reseller_token_count, sender=Instagram)
