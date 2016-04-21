from __future__ import unicode_literals

from django.db import models
# Create your models here.


class TimeAuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At',
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Modified At',
                                      editable=False)

    class Meta:
        abstract = True


