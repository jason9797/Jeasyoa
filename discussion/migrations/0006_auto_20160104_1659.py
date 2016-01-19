# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0005_auto_20160104_1658'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([]),
        ),
    ]
