# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 18:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20170108_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 8, 19, 58, 15, 816428), verbose_name='Date of transaction'),
        ),
    ]