# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 21:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_auto_20170113_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 13, 21, 56, 44, 248662, tzinfo=utc), verbose_name='Date of transaction'),
        ),
    ]