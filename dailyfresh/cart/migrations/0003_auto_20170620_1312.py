# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartinfo_isdelete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartinfo',
            name='isDelete',
            field=models.BooleanField(default=1),
        ),
    ]
