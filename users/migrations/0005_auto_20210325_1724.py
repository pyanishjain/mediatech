# Generated by Django 3.0.3 on 2021-03-25 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210325_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagram',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='whatsapp',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
    ]