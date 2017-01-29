# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 20:47
from __future__ import unicode_literals

import datetime

import django.db.models.deletion
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0007_auto_20170122_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.Category'),
        ),
        migrations.AlterField(
            model_name='budget',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2017, 1, 22, 20, 47, 2, 221210, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2017, 1, 22, 20, 47, 2, 221210, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.Wallet'),
        ),
    ]
