# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20170620_1137'),
        ('userlogin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orderid', models.IntegerField()),
                ('ocartid', models.IntegerField()),
                ('ogprice', models.DecimalField(max_digits=6, decimal_places=2)),
                ('ototal', models.DecimalField(max_digits=6, decimal_places=2)),
                ('paystatic', models.BooleanField(default=0)),
                ('ogid', models.ForeignKey(to='goods.GoodsInfo')),
                ('ouserid', models.ForeignKey(to='userlogin.user')),
            ],
        ),
    ]
