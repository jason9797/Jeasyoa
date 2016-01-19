# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0009_auto_20160105_0937'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comments',
            unique_together=set([('content', 'post', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('title', 'author')]),
        ),
    ]
