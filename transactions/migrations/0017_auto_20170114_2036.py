# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 19:36
from __future__ import unicode_literals

import datetime

import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0016_auto_20170114_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 14, 19, 36, 30, 914097, tzinfo=utc), verbose_name='Date of transaction'),
        ),
    ]
