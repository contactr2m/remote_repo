from django.contrib import admin
from guardian.admin import GuardedModelAdmin

# Register your models here.


class BaseAdmin(GuardedModelAdmin):

    search_fields = ['name']
    save_on_top = True
