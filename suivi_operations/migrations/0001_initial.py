# Generated by Django 4.2.2 on 2023-06-21 01:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(help_text='This email also serves as the main login.', max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('gender', models.CharField(choices=[('M', 'Men'), ('W', 'Women'), ('U', 'Unspecified')], default='U', help_text='Gender choices are limited to existing Ultimate categories.', max_length=1, verbose_name='gender')),
                ('phone_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='phone number')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='ProfileAC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idContact', models.PositiveIntegerField(default=None, null=True, unique=True, verbose_name='contact identifier')),
                ('member_revo', models.BooleanField(default=False, verbose_name="revolution'air membership")),
                ('member_CS', models.BooleanField(default=False, verbose_name='Championnet Sports membership')),
                ('detail_url', models.URLField(blank=True, verbose_name='detail url')),
                ('last_check', models.DateField(default=datetime.date.today, verbose_name='last check')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_ac', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
