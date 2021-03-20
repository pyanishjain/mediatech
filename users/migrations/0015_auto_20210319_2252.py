# Generated by Django 3.0.3 on 2021-03-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210319_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegram',
            name='confirm_paid',
            field=models.BooleanField(default=False, help_text='do not fill this field'),
        ),
        migrations.AlterField(
            model_name='instagram',
            name='confirm_paid',
            field=models.BooleanField(default=False, help_text='do not fill this field'),
        ),
        migrations.AlterField(
            model_name='whatsapp',
            name='confirm_paid',
            field=models.BooleanField(default=False, help_text='do not fill this field'),
        ),
    ]
