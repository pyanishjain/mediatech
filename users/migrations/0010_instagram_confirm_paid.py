# Generated by Django 3.0.3 on 2021-03-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_software_telegram_class_xpath'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagram',
            name='confirm_paid',
            field=models.BooleanField(default=False),
        ),
    ]
