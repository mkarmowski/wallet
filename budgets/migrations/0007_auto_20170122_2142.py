# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 20:42
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0006_auto_20170121_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='completion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='budget',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2017, 1, 22, 20, 42, 15, 119756, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2017, 1, 22, 20, 42, 15, 119756, tzinfo=utc)),
        ),
    ]
