# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0002_auto_20151211_2358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knote',
            old_name='knote_data',
            new_name='knote_date',
        ),
    ]
