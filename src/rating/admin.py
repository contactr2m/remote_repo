from django.contrib import admin

from rating.models import Vote
# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True


class VoteAdmin(BaseAdmin):
    pass

admin.site.register(Vote, VoteAdmin)
