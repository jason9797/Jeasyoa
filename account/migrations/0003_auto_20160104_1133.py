# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151222_0309'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'department', 'verbose_name_plural': 'departments'},
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ('content_type__app_label', 'content_type__model', 'codename'), 'verbose_name': 'access permission', 'verbose_name_plural': 'access permissions'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Account', 'verbose_name_plural': 'Accounts'},
        ),
        migrations.AlterField(
            model_name='permission',
            name='display',
            field=models.BooleanField(default=False, verbose_name='show in front end'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='date_of_birth', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='departments',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='account.Department', blank=True, help_text='The departments this user belongs to. A user will get all permissions granted to each of their departments.', verbose_name='department'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=255, verbose_name='email', validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is_active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='is_admin'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=20, null=True, verbose_name='name', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message='must be digit')], max_length=15, blank=True, unique=True, verbose_name='phone_number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='user_photo', null=True, verbose_name='user_photo', blank=True),
        ),
    ]
