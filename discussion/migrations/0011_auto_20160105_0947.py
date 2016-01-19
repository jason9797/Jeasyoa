# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0010_auto_20160105_0938'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comments',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([]),
        ),
    ]
