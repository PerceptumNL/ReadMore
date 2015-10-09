# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userprofile_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
