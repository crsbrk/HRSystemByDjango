from django.contrib import admin

# Register your models here.
from .models import Cutovers
from accounts.workers import make_worker_admin_form

class CutoversAdmin(admin.ModelAdmin):
    form = make_worker_admin_form(Cutovers, leader_fields=('pj_leader',))
    list_display = ('cutover_num','title','pj_leader','is_not_delayed','deadline_at')
    search_fields = ('cutover_num','title','pj_leader','deadline_at',)
    list_display_links = ('cutover_num','title',)
    list_filter = ('pj_leader','is_not_delayed',)
    list_per_page = 25
admin.site.register(Cutovers, CutoversAdmin)
