from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
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
    content_object = GenericForeignKey('content_type', 'object_id')

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

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Manager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation



def limit_total_votes(num):
    from rating.models import Vote

    def total_vote_limiter(request, content_type, object_id, vote):
        return Vote.objects.filter(content_type=content_type,
                                   token=request.rating_token).count() < num
    return total_vote_limiter


def enable_voting_on(cls, manager_name='objects', votes_name='votes', upvotes_name='total_upvotes',
                     downvotes_name='total_downvotes', total_name='vote_total',
                     add_vote_name='add_vote', remove_vote_name='remove_vote', base_manager=None):
    from rating.models import Vote
    VOTE_TABLE = Vote._meta.db_table

    def add_vote(self, token, vote):
        voteobj, created = self.votes.get_or_create(token=token,
                                                    defaults={'vote': vote,
                                                              'content_object': self})
        if not created:
            voteobj.vote = vote
            voteobj.save()

    def remove_vote(self, token):
        self.votes.filter(token=token).delete()

    def get_total(self):
        return getattr(self, upvotes_name) - getattr(self, downvotes_name)

    if base_manager is None:
        if hasattr(cls, manager_name):
            base_manager = getattr(cls, manager_name).__class__
        else:
            base_manager = Manager

    class VotableManager(base_manager):

        def get_queryset(self):
            db_table = self.model._meta.db_table
            pk_name = self.model._meta.pk.attname
            content_type = ContentType.objects.get_for_model(self.model).id
            downvote_query = '(SELECT COUNT(*) from %s WHERE vote=-1 AND object_id=%s.%s AND content_type_id=%s)' % (VOTE_TABLE, db_table, pk_name, content_type)
            upvote_query = '(SELECT COUNT(*) from %s WHERE vote=1 AND object_id=%s.%s AND content_type_id=%s)' % (VOTE_TABLE, db_table, pk_name, content_type)
            return super(VotableManager, self).get_queryset().extra(
                select={upvotes_name: upvote_query,
                        downvotes_name: downvote_query})

        def from_token(self, token):
            db_table = self.model._meta.db_table
            pk_name = self.model._meta.pk.attname
            content_type = ContentType.objects.get_for_model(self.model).id
            query = '(SELECT vote from %s WHERE token=%%s AND object_id=%s.%s AND content_type_id=%s)' % (VOTE_TABLE, db_table, pk_name, content_type)
            return self.get_queryset().extra(select={'user_vote': query},
                                             select_params=(token,))

        def from_request(self, request):
            if not hasattr(request, 'rating_token'):
                raise ImproperlyConfigured('To use rating a ratingMiddleware must be installed. '
                                           '(see rating/middleware.py)')
            return self.from_token(request.rating_token)

    cls.add_to_class('objects', VotableManager())
    cls.add_to_class(votes_name, GenericRelation(Vote))
    cls.add_to_class(total_name, property(get_total))
    cls.add_to_class(add_vote_name, add_vote)
    cls.add_to_class(remove_vote_name, remove_vote)
    cls.add_to_class("whatever", "whatever_vote")
