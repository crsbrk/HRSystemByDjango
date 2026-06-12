from django.contrib import admin

# Register your models here.
from .models import Orders
from accounts.workers import make_worker_admin_form

class OrdersAdmin(admin.ModelAdmin):
    form = make_worker_admin_form(Orders, leader_fields=('pj_leader',), optional_fields=('pj_participant1','pj_participant2','pj_participant3'))
    list_display = ('orders_num','title','pj_score','is_finished','is_not_delayed','orders_type','deadline_at','pj_leader','workload_allot','pj_participant1','workload_allot1','pj_participant2','workload_allot2','pj_participant3','workload_allot3')
    list_per_page = 10
    list_filter = ('orders_type','is_finished','is_not_delayed',)
    list_editable =('orders_type','is_finished','is_not_delayed',)
    search_fields = ('orders_num','title','pj_leader','pj_participant1','pj_participant2','pj_participant3',)
    readonly_fields = ("created_at",)

admin.site.register(Orders, OrdersAdmin)
admin.site.site_header = "人力考核系统"
admin.site.site_title = "考核系统"
