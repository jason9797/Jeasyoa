# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.contrib.auth.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80, verbose_name='name')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('codename', models.CharField(max_length=100, verbose_name='codename')),
                ('display', models.BooleanField(default=False, verbose_name='display_or_not')),
                ('display_name', models.CharField(max_length=255, null=True, verbose_name='display_name', blank=True)),
                ('content_type', models.ForeignKey(related_name='content_types', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('content_type__app_label', 'content_type__model', 'codename'),
                'verbose_name': 'permission',
                'verbose_name_plural': 'permissions',
            },
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='\u90ae\u7bb1\u5730\u5740/\u624b\u673a\u53f7\u7801', validators=[django.core.validators.EmailValidator])),
                ('name', models.CharField(max_length=20, null=True, verbose_name='\u540d\u79f0', blank=True)),
                ('phone_number', models.CharField(null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message='must be digit')], max_length=15, blank=True, unique=True, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('date_of_birth', models.DateField(null=True, verbose_name='\u51fa\u751f\u65e5\u671f', blank=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='\u6d3b\u52a8')),
                ('is_admin', models.BooleanField(default=False, verbose_name='\u7ba1\u7406\u5458')),
                ('user_image', easy_thumbnails.fields.ThumbnailerImageField(upload_to='user_photo', null=True, verbose_name='\u5934\u50cf', blank=True)),
                ('image_height', models.PositiveIntegerField(default='50', null=True, editable=False, blank=True)),
                ('image_width', models.PositiveIntegerField(default='50', null=True, editable=False, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('departments', models.ManyToManyField(related_query_name='user', related_name='user_set', to='account.Department', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='account.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='permissions',
            field=models.ManyToManyField(to='account.Permission', verbose_name='permissions', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together=set([('content_type', 'codename')]),
        ),
    ]
