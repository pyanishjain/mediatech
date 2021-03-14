from django.db import models
from django.contrib.auth.models import User
import dateutil.relativedelta as delta


class Plan(models.Model):
    duration = models.IntegerField(null=True, help_text='Enter Months')
    locationCount = models.IntegerField(null=True, blank=True)
    keywordCount = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.duration.__str__() + '-' + self.locationCount.__str__() + '-' + self.keywordCount.__str__()


class Software(models.Model):
    telegram = models.FileField(upload_to='software', null=True, blank=True)
    whatsapp = models.FileField(upload_to='software', null=True, blank=True)
    instagram = models.FileField(upload_to='software', null=True, blank=True)


class Reseller(models.Model):
    reseller = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    token_count = models.IntegerField(default=10)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.reseller.__str__()


class Profile(models.Model):
    reseller = models.ForeignKey(
        Reseller, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phoneNo = models.IntegerField(null=True)
    unhash_password = models.CharField(null=True, blank=True, max_length=256)
    ip_address = models.CharField(
        null=True, blank=True, max_length=256, help_text='do not fill this field')

    def __str__(self):
        return self.user.__str__()


class Base(models.Model):
    def createLicenceExpireDate(self):
        duration = self.plan.duration
        x = self.licenceExpireDate = self.date_updated + \
            delta.relativedelta(months=int(duration))
        return x

    def save(self, *args, **kwargs):
        if self.isPaid:
            self.licenceExpireDate = self.createLicenceExpireDate()

        else:
            self.licenceExpireDate = self.DemoDate

        super().save(*args, **kwargs)


class Telegram(Base):
    reseller = models.ForeignKey(
        Reseller, null=True, blank=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, null=True, blank=True)

    DemoDate = models.DateField(null=True, blank=True)
    licenceExpireDate = models.DateField(null=True, blank=True)
    isPaid = models.BooleanField(
        default=False, blank=True, help_text='only click when amount is paid')
    isActive = models.BooleanField(default=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.profile)


class Whatsapp(Base):
    reseller = models.ForeignKey(
        Reseller, null=True, blank=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, null=True, blank=True)

    DemoDate = models.DateField(null=True, blank=True)
    licenceExpireDate = models.DateField(null=True, blank=True)
    isPaid = models.BooleanField(
        default=False, blank=True, help_text='only click when amount is paid')
    isActive = models.BooleanField(default=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.profile)


class Instagram(Base):
    reseller = models.ForeignKey(
        Reseller, null=True, blank=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, null=True, blank=True)

    DemoDate = models.DateField(null=True, blank=True)
    licenceExpireDate = models.DateField(null=True, blank=True)
    isPaid = models.BooleanField(
        default=False, blank=True, help_text='only click when amount is paid')
    isActive = models.BooleanField(default=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.profile)
