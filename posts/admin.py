from django.contrib import admin

# Register your models here.

from .models import Posts

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title','pj_score','deadline_at','is_not_delayed','pj_progress','pj_leader','workload_allot','pj_participant1','workload_allot1','pj_participant2','workload_allot2','pj_participant3','workload_allot3')
    list_per_page = 25
    search_fields = ('title','pj_leader','pj_participant1','pj_participant2','pj_participant3','deadline_at',)
    list_filter = ('pj_score','is_not_delayed',)
#    list_display = ('title','pj_score','pj_leader','pj_progress','is_delayed','deadline_at')
admin.site.register(Posts, PostsAdmin)
