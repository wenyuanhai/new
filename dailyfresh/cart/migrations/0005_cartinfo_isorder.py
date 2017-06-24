# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20170621_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartinfo',
            name='isOrder',
            field=models.BooleanField(default=0),
        ),
    ]
