# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-02-21 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avm', '0007_auto_20200221_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='init_date',
            field=models.DateTimeField(null=True),
        ),
    ]
