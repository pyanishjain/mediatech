# Generated by Django 3.0.3 on 2021-03-13 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagram',
            name='isActive',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='telegram',
            name='isActive',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='whatsapp',
            name='isActive',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
