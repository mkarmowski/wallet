# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 16:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0004_auto_20170117_1730'),
        ('transactions', '0018_auto_20170116_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='budget',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Budget'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 17, 16, 30, 56, 530415, tzinfo=utc), verbose_name='Date of transaction'),
        ),
    ]