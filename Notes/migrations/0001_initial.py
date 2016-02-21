# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('knote_title', models.CharField(max_length=200)),
                ('knote_note', models.TextField()),
                ('knote_data', models.DateTimeField()),
                ('knote_likes', models.IntegerField()),
            ],
            options={
                'db_table': 'KNote',
            },
        ),
    ]
