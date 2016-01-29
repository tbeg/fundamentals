from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models as gismodels
from decimal import Decimal
from django.utils import timezone

from django.template import Context, loader
from hendrix.contrib.async.signals import message_signal


class House(models.Model):
    id = models.AutoField(primary_key=True)
    fuid = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    strnumr = models.CharField(max_length=255, blank=True, null=True)
    postcod = models.CharField(max_length=7, blank=True, null=True)
    plaprov = models.CharField(max_length=255, blank=True, null=True)
    woonopp = models.IntegerField(blank=True, null=True)
    percopp = models.IntegerField(blank=True, null=True)
    vrprijs = models.IntegerField(blank=True, null=True)
    sqprijs = models.FloatField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    dellink = models.CharField(max_length=255, blank=True, null=True)
    rdx = models.CharField(max_length=255, blank=True, null=True)
    rdy = models.CharField(max_length=255, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.000000'))
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.000000'))
    sender = models.CharField(max_length=100, default='')
    channel = models.CharField(max_length=100, db_index=True, default='homepage')
    content = models.TextField('enter a message', default='')
    date_created = models.DateTimeField(default=timezone.now)
    geom = gismodels.PointField(blank=True, null=True)
    objects = gismodels.GeoManager()

    class Meta:
        managed = True
        db_table = 'house'


def save_chat_message(*args, **kwargs):

    """
    kwargs will always include:

     'data':
        # will always be exactly what your client sent on the socket
        # in this case...
        {u'message': u'hi', u'sender': u'anonymous', u'channel': u'homepage'},

     'dispatcher':
        # the dispatcher that will allow for broadcasting a response
      <hendrix.contrib.async.messaging.MessageDispatcher object at 0x10ddb1c10>,

    """

    data = kwargs.get('data')
    #import pdb;pdb.set_trace()
    if data.get('message') and data.get('channel'):

        cm = House.objects.create(
            sender=data.get('sender'),
            content=data.get('message'),
            channel=data.get('channel')
        )

        t = loader.get_template('message.html')

        # now send broadcast a message back to anyone listening
        # on the channel
        kwargs.get('dispatcher').send(cm.channel, {
            'html': t.render(Context({'message': cm}))
        })

message_signal.connect(save_chat_message)
