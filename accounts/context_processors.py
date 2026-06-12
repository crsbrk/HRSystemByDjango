from .models import SiteSetting, UserProfileInfo, WorkApplication


def site_settings(request):
    return {
        'site_settings': SiteSetting.load(),
    }


def approval_badge(request):
    """给审批人提供待办数量与角色标记，用于拓扑栏入口展示。"""
    data = {'pending_approval_count': 0, 'is_reviewer': False}
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and not user.is_superuser:
        try:
            role = user.userprofileinfo.role
        except UserProfileInfo.DoesNotExist:
            role = 'employee'
        data['is_reviewer'] = role in ('manager', 'approver')
        data['pending_approval_count'] = WorkApplication.objects.filter(
            reviewer=user, status='pending').count()
    return data
