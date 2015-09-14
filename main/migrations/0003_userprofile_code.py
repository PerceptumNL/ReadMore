# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150911_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='code',
            field=models.ForeignKey(blank=True, to='main.TeacherCode', null=True),
        ),
    ]
