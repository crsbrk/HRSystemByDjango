from django.contrib import admin

from .models import Bonuses


class BonusesAdmin(admin.ModelAdmin):
    list_display = ('title','pj_score','created_at','is_not_delayed','pj_leader','workload_allot','pj_participant1','workload_allot1','pj_participant2','workload_allot2','pj_participant3','workload_allot3')
    list_per_page = 25
    search_fields = ('title','pj_score','pj_leader','pj_participant1','pj_participant2','pj_participant3','created_at',)


admin.site.register(Bonuses, BonusesAdmin)
