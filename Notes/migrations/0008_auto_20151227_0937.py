# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0007_auto_20151227_0112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knote',
            old_name='knote_likes',
            new_name='knote_views',
        ),
    ]
