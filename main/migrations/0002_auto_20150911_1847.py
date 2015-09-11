# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachercode',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='teachercode',
            name='created_on',
            field=models.DateField(default=datetime.datetime(2015, 9, 11, 18, 46, 49, 671703, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teachercode',
            name='institute',
            field=models.ForeignKey(default=1, to='main.Institute'),
            preserve_default=False,
        ),
    ]
