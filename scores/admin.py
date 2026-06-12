from django.contrib import admin

from .models import Scores, DemocracyRating

class ScoresAdmin(admin.ModelAdmin):
    list_display = ('worker_name','score_year_month','score_posts','score_orders','score_bonuses','score_cutovers','score_routine','score_faulty')


class DemocracyRatingAdmin(admin.ModelAdmin):
    list_display = ('evaluator', 'target', 'year_season', 'attitude', 'responsibility', 'discipline')
    list_filter = ('year_season',)
    search_fields = ('evaluator__username', 'target__username')


admin.site.register(Scores, ScoresAdmin)
admin.site.register(DemocracyRating, DemocracyRatingAdmin)
