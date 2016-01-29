# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 16:59
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='channel',
            field=models.CharField(db_index=True, default='homepage', max_length=100),
        ),
        migrations.AddField(
            model_name='house',
            name='content',
            field=models.TextField(default='', verbose_name='enter a message'),
        ),
        migrations.AddField(
            model_name='house',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='house',
            name='sender',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='house',
            name='fuid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='house',
            name='percopp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='sqprijs',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='vrprijs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='woonopp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
