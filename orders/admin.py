from django.contrib import admin

# Register your models here.
from .models import Orders

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orders_num','title','pj_score','is_finished','pj_leader','workload_allot','pj_participant1','workload_allot1','pj_participant2','workload_allot2','pj_participant3','workload_allot3')
admin.site.register(Orders, OrdersAdmin)
admin.site.site_header = "分组网人力考核系统"
admin.site.site_title = "考核系统"
