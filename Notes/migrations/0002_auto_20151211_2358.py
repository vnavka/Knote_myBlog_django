# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'Comments',
            },
        ),
        migrations.AlterField(
            model_name='knote',
            name='knote_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comments',
            name='comment_note',
            field=models.ForeignKey(to='Notes.KNote'),
        ),
    ]
