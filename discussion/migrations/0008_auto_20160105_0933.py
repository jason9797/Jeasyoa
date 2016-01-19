# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0007_auto_20160104_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='name'),
        ),
        migrations.AlterUniqueTogether(
            name='comments',
            unique_together=set([('content', 'post', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('title', 'author')]),
        ),
    ]
