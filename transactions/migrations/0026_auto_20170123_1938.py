# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 18:38
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0025_auto_20170123_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 23, 18, 38, 58, 190532, tzinfo=utc), verbose_name='Date of transaction'),
        ),
    ]
