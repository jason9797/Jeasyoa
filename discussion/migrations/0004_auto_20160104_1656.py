# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_auto_20160104_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='comments',
            unique_together=set([('content', 'post', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('title',)]),
        ),
    ]
