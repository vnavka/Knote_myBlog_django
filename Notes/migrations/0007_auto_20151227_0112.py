# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0006_userimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_login',
            field=models.CharField(default=b'guest', max_length=300),
        ),
        migrations.AlterField(
            model_name='userimage',
            name='user_image_pass',
            field=models.CharField(default=b'/static/media/def.png', max_length=200),
        ),
    ]
