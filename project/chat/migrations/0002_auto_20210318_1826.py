# Generated by Django 3.1.7 on 2021-03-18 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='message_status',
            field=models.CharField(max_length=12),
        ),
    ]