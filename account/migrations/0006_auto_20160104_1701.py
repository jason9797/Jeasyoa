# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20160104_1656'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([]),
        ),
    ]
