from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models
from django.conf import settings
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    avatar_url = models.CharField(max_length=256, blank=True, null=True)
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verified", default=False)
    dob = models.DateField(verbose_name="dob", blank=True, null=True)

    class Meta:
        abstract = True
        db_table = 'user_profile'

    def __str__(self):
        return force_text(self.user.email)


@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{}'s profile". format(self.user)

    # def account_verified(self):
    #     if self.user.is_authenticated:
    #         result = EmailAddress.objects.filter(email=self.user.email)
    #         if len(result):
    #             return result[0].verified
    #     return False

