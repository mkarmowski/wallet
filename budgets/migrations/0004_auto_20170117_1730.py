# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 16:30
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_auto_20170116_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2017, 1, 17, 16, 30, 56, 527412, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2017, 1, 17, 16, 30, 56, 527412, tzinfo=utc)),
        ),
    ]
