from django.contrib import admin

# Register your models here.

from .models import Faulty


class FaultyAdmin(admin.ModelAdmin):
    list_display = ('title', 'pj_score','pj_type', 'is_not_delayed', 'pj_leader', 'workload_allot', 'pj_participant1',
                    'workload_allot1', 'pj_participant2', 'workload_allot2', 'pj_participant3', 'workload_allot3')
    list_per_page = 25
    list_filter = ('pj_type','created_at')
    search_fields = ('title', 'pj_score', 'pj_leader','pj_type',
                     'pj_participant1', 'pj_participant2', 'pj_participant3','created_at',)


admin.site.register(Faulty, FaultyAdmin)
