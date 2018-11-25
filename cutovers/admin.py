from django.contrib import admin

# Register your models here.
from .models import Cutovers

class CutoversAdmin(admin.ModelAdmin):
    list_display = ('cutover_num','title','pj_leader','is_delayed','deadline_at')
admin.site.register(Cutovers, CutoversAdmin)
