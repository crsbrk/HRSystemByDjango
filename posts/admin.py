from django.contrib import admin

# Register your models here.

from .models import Posts

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title','pj_score','pj_leader','pj_progress','is_delayed','deadline_at')
admin.site.register(Posts, PostsAdmin)
