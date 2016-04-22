from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.conf import settings
from core.models import TimeAuditModel
# Create your models here.

VOTE_CHOICES = (
    (+1, '+1'),
    (-1, '-1'),
)


class Vote(TimeAuditModel):
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="votes")

    # generic foreign key to the model being voted upon
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'rating'
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        unique_together = (('user', 'content_type', 'object_id'),)

        permissions = (
            ('vote_for_user', 'Can vote in behalf of other user'),
        )

    def __unicode__(self):
        return '%s from %s on %s' % (self.get_vote_display(), self.user,
                                     self.content_object)


# def post_save_vote(sender, **kwargs):
#     obj = kwargs['instance']
#     try:
#         from pushy.util import pushy_custom
#         pushy_custom(obj.content_object.get_api_url(), type='update')
#     except Exception, e:
#         print e

# post_save.connect(post_save_vote, sender=Vote)
