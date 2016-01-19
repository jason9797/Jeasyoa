# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import account.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '\u90e8\u95e8', 'verbose_name_plural': '\u90e8\u95e8'},
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ('content_type__app_label', 'content_type__model', 'codename'), 'verbose_name': '\u8bbf\u95ee\u6743\u9650', 'verbose_name_plural': '\u8bbf\u95ee\u6743\u9650'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='permission',
            name='display_name',
        ),
        migrations.AlterField(
            model_name='permission',
            name='display',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5728\u524d\u7aef\u663e\u793a'),
        ),
    ]
