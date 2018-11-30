from django.contrib import admin

# Register your models here.

from .models import Bonuses


class BonusesAdmin(admin.ModelAdmin):
    list_display = ('title','pj_score','is_delayed','pj_leader','workload_allot','pj_participant1','workload_allot1','pj_participant2','workload_allot2','pj_participant3','workload_allot3')

    #list_display = ('orders_num','title','pj_score','is_delayed','created_at')
admin.site.register(Bonuses, BonusesAdmin)
