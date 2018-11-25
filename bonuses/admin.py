from django.contrib import admin

# Register your models here.

from .models import Bonuses


class BonusesAdmin(admin.ModelAdmin):
    list_display = ('title','pj_score','is_delayed','created_at')
admin.site.register(Bonuses, BonusesAdmin)
