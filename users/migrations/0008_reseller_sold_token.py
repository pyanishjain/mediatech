# Generated by Django 3.0.3 on 2021-03-16 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_whatsapp_confirm_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='reseller',
            name='sold_token',
            field=models.IntegerField(default=0),
        ),
    ]
