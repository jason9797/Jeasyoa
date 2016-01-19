# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0006_auto_20160104_1659'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([]),
        ),
    ]
