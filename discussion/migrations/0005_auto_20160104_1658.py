# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0004_auto_20160104_1656'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comments',
            unique_together=set([]),
        ),
    ]
