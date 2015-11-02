# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userprofile_is_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='email_domain',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
