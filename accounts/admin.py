from django.contrib import admin
from django.db import models
from django.forms import Textarea

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.utils import timezone

from .models import HomeSlide, SiteSetting, UserProfileInfo, User, WorkApplication
from .services import (
    delete_application_work_item,
    refresh_scores_for_application,
    sync_application_work_item,
)


# Register your models here.
#admin.site.register(UserProfileInfo)

class ProfileInline(admin.StackedInline):
    model = UserProfileInfo
    can_delete = False
    verbose_name_plural = '附加信息'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'footer_text', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 24, 'cols': 100, 'style': 'font-family:monospace;'})},
    }

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()


@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order', 'is_active', 'created_at')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('title', 'subtitle')
    list_filter = ('is_active',)


@admin.register(WorkApplication)
class WorkApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'applicant', 'work_type', 'score', 'status', 'reviewer', 'created_at')
    list_filter = ('status', 'work_type', 'created_at')
    search_fields = ('title', 'applicant__username', 'description')
    readonly_fields = ('created_at', 'reviewed_at', 'materialized_model', 'materialized_object_id')
    actions = ('approve_applications', 'reject_applications')

    def save_model(self, request, obj, form, change):
        previous_application = None
        if obj.pk:
            previous_application = WorkApplication.objects.filter(
                pk=obj.pk).select_related('applicant').first()

        if obj.status in ('approved', 'rejected'):
            if not obj.reviewer:
                obj.reviewer = request.user
            if not obj.reviewed_at:
                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

        if previous_application and previous_application.status == 'approved':
            delete_application_work_item(previous_application)
            refresh_scores_for_application(previous_application)
        if obj.status == 'approved':
            sync_application_work_item(obj)
            refresh_scores_for_application(obj)

    def approve_applications(self, request, queryset):
        updated = 0
        for application in queryset.select_related('applicant'):
            application.status = 'approved'
            application.reviewer = request.user
            application.reviewed_at = timezone.now()
            application.save(update_fields=['status', 'reviewer', 'reviewed_at'])
            sync_application_work_item(application)
            refresh_scores_for_application(application)
            updated += 1
        self.message_user(request, '已审批通过 %s 条申请，并刷新对应月份积分。' % updated)

    approve_applications.short_description = '审批通过选中的申请'

    def reject_applications(self, request, queryset):
        updated = 0
        for application in queryset.select_related('applicant'):
            was_approved = application.status == 'approved'
            application.status = 'rejected'
            application.reviewer = request.user
            application.reviewed_at = timezone.now()
            application.save(update_fields=['status', 'reviewer', 'reviewed_at'])
            if was_approved:
                delete_application_work_item(application)
                refresh_scores_for_application(application)
            updated += 1
        self.message_user(request, '已驳回 %s 条申请，并同步刷新积分。' % updated)

    reject_applications.short_description = '驳回选中的申请'
