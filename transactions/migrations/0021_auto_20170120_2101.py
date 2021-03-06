# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 20:01
from __future__ import unicode_literals

import datetime

import django.db.models.deletion
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0005_auto_20170120_2101'),
        ('transactions', '0020_auto_20170117_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='saving',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Saving'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 20, 20, 1, 56, 246688, tzinfo=utc), verbose_name='Date of transaction'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='notes',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]
