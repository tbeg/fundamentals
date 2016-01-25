from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models as gismodels
from decimal import Decimal


class House(models.Model):
    id = models.AutoField(primary_key=True)
    fuid = models.IntegerField()
    image = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    strnumr = models.CharField(max_length=255, blank=True, null=True)
    postcod = models.CharField(max_length=7, blank=True, null=True)
    plaprov = models.CharField(max_length=255, blank=True, null=True)
    woonopp = models.IntegerField()
    percopp = models.IntegerField()
    vrprijs = models.IntegerField()
    sqprijs = models.FloatField()
    link = models.CharField(max_length=255, blank=True, null=True)
    dellink = models.CharField(max_length=255, blank=True, null=True)
    rdx = models.CharField(max_length=255, blank=True, null=True)
    rdy = models.CharField(max_length=255, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.000000'))
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.000000'))
    geom = gismodels.PointField()
    objects = gismodels.GeoManager()

    class Meta:
        managed = True
        db_table = 'house'
