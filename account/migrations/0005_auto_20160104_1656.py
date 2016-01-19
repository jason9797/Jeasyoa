# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20160104_1344'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('email', 'phone_number')]),
        ),
    ]
