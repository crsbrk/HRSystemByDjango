from django.contrib import admin

from .models import Scores

class ScoresAdmin(admin.ModelAdmin):
    list_display = ('worker_name','score_year_month','score_posts','score_orders','score_bonuses','score_cutovers','score_routine','score_faulty')
#    list_display = ('title','pj_score','pj_leader','pj_progress','is_delayed','deadline_at')
admin.site.register(Scores, ScoresAdmin)
