# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 18:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20170108_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 8, 19, 49, 13, 196529), verbose_name='Date of transaction'),
        ),
    ]
