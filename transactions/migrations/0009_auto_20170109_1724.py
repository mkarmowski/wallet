# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 16:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_auto_20170108_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], default='expense', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 17, 24, 11, 781512), verbose_name='Date of transaction'),
        ),
    ]