# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 20:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0008_auto_20170122_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2017, 2, 11, 20, 15, 56, 689306, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2017, 2, 11, 20, 15, 56, 689306, tzinfo=utc)),
        ),
    ]
