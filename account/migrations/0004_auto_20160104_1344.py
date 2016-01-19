# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160104_1133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'Department', 'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ('content_type__app_label', 'content_type__model', 'codename'), 'verbose_name': 'Access permission', 'verbose_name_plural': 'Access permissions'},
        ),
        migrations.AlterField(
            model_name='department',
            name='permissions',
            field=models.ManyToManyField(to='account.Permission', verbose_name='Permissions', blank=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='content_type',
            field=models.ForeignKey(related_name='content_types', verbose_name='Content_type', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='Date_of_birth', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='departments',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='account.Department', blank=True, help_text='The departments this user belongs to. A user will get all permissions granted to each of their departments.', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=255, verbose_name='Email', validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=20, null=True, verbose_name='Name', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message='must be digit')], max_length=15, blank=True, unique=True, verbose_name='Phone_number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='user_photo', null=True, verbose_name='User_photo', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='account.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='User permissions'),
        ),
    ]
