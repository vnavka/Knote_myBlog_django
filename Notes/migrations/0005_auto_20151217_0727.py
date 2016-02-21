# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0004_knote_knote_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knote',
            old_name='Knote_host',
            new_name='knote_host',
        ),
    ]
