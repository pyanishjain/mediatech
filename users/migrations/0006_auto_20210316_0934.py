# Generated by Django 3.0.3 on 2021-03-16 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_whatsapp_class_xpath'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whatsapp',
            name='class_xpath',
        ),
        migrations.AddField(
            model_name='software',
            name='whatsapp_class_xpath',
            field=models.TextField(blank=True, null=True),
        ),
    ]
