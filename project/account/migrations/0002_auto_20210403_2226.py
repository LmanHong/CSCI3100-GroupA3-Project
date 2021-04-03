# Generated by Django 3.1.7 on 2021-04-03 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Uncertain')], default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='job_title',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='passions',
            field=models.CharField(default=None, help_text='hiking, outdoors, cat lover', max_length=256, null=True),
        ),
    ]
