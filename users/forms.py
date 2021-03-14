from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             max_length=254, help_text='Required. Inform a valid email address.')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')

    class Meta:
        model = User
        fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    phoneNo = forms.IntegerField()

    class Meta:
        model = Profile
        fields = ('phoneNo',)


class PlanForm(forms.ModelForm):
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())

    class Meta:
        model = Plan
        fields = ('plan',)


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')


class TelegramForm(forms.ModelForm):
    class Meta:
        model = Telegram
        fields = '__all__'
        widgets = {'reseller': forms.HiddenInput(),
                   'profile': forms.HiddenInput(),
                   'DemoDate': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
                   'licenceExpireDate': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
                   }


class WhatsappForm(forms.ModelForm):
    class Meta:
        model = Whatsapp
        fields = '__all__'
        widgets = {'reseller': forms.HiddenInput(),
                   'profile': forms.HiddenInput(),
                   'DemoDate': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
                   'licenceExpireDate': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
                   }


class InstagramForm(forms.ModelForm):
    class Meta:
        model = Instagram
        fields = '__all__'
        widgets = {'reseller': forms.HiddenInput(),
                   'profile': forms.HiddenInput(),
                   'DemoDate': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
                   'licenceExpireDate': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
                   }
