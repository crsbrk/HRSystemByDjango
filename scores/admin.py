from django.contrib import admin

from .models import (
    DemocracyRating,
    ScoreCategoryRule,
    ScoreFormulaPolicy,
    ScoreRankingSnapshot,
    Scores,
)

class ScoresAdmin(admin.ModelAdmin):
    list_display = ('worker_name','score_year_month','score_posts','score_orders','score_bonuses','score_cutovers','score_routine','score_faulty')


class DemocracyRatingAdmin(admin.ModelAdmin):
    list_display = ('evaluator', 'target', 'year_season', 'attitude', 'responsibility', 'discipline')
    list_filter = ('year_season',)
    search_fields = ('evaluator__username', 'target__username')


class ScoreCategoryRuleInline(admin.TabularInline):
    model = ScoreCategoryRule
    extra = 0


@admin.register(ScoreFormulaPolicy)
class ScoreFormulaPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ranking_formula', 'effective_year', 'effective_month', 'is_active', 'updated_at')
    list_filter = ('ranking_formula', 'is_active', 'effective_year')
    search_fields = ('name', 'notes')
    inlines = (ScoreCategoryRuleInline,)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ScoreRankingSnapshot)
class ScoreRankingSnapshotAdmin(admin.ModelAdmin):
    list_display = ('worker_name', 'score_year', 'score_month', 'rank', 'work_score', 'democracy_score', 'total_score', 'policy')
    list_filter = ('score_year', 'score_month', 'policy')
    search_fields = ('worker_name',)
    readonly_fields = (
        'worker_name', 'score_year', 'score_month',
        'raw_posts', 'raw_orders', 'raw_cutovers', 'raw_bonuses', 'raw_faulty', 'raw_routine',
        'final_posts', 'final_orders', 'final_cutovers', 'final_bonuses', 'final_faulty', 'final_routine',
        'work_score', 'democracy_score', 'total_score', 'rank', 'policy', 'policy_snapshot',
        'created_at', 'updated_at',
    )


admin.site.register(Scores, ScoresAdmin)
admin.site.register(DemocracyRating, DemocracyRatingAdmin)
