from django.contrib import admin

# Register your models here.
from .models import Cutovers

class CutoversAdmin(admin.ModelAdmin):
    list_display = ('cutover_num','title','pj_leader','is_delayed','deadline_at')
    search_fields = ('cutover_num','title','pj_leader',)
    list_filter = ('pj_leader','is_delayed',)
    list_per_page = 25
admin.site.register(Cutovers, CutoversAdmin)
