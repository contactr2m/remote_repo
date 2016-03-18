# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 17:15
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0005_auto_20160317_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='type',
            field=select_multiple_field.models.SelectMultipleField(choices=[('Singer', 'Singer'), ('MusicDirector', 'MusicDirector'), ('Lyricist', 'Lyricist')], max_length=15),
        ),
    ]
