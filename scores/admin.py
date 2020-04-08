from django.contrib import admin

from .models import Scores,Attitude,Responsibility,Discipline

class ScoresAdmin(admin.ModelAdmin):
    list_display = ('worker_name','score_year_month','score_posts','score_orders','score_bonuses','score_cutovers','score_routine','score_faulty')
#    list_display = ('title','pj_score','pj_leader','pj_progress','is_delayed','deadline_at')

class AttitudeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Attitude._meta.get_fields()]
class ResponsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Responsibility._meta.get_fields()]
class DiscipAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Discipline._meta.get_fields()]

admin.site.register(Scores, ScoresAdmin)
admin.site.register(Attitude, AttitudeAdmin)
admin.site.register(Responsibility, ResponsAdmin)
admin.site.register(Discipline, DiscipAdmin)
