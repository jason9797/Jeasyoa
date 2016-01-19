# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0008_auto_20160105_0933'),
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
