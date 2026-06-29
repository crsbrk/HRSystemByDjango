import re

from django.db.models import Q
from django.utils import timezone


def normalize_title(value):
    value = value or ''
    return re.sub(r'\s+', '', value).lower()


def normalized_work_date(application):
    if application.work_date:
        return application.work_date
    if application.created_at:
        return application.created_at.date()
    return None


def build_duplicate_signature(application):
    date_value = normalized_work_date(application)
    number_or_title = (application.work_num or normalize_title(application.title)).strip()
    return '|'.join([
        application.work_type or '',
        number_or_title,
        str(date_value or ''),
        str(application.applicant_id or ''),
        str(application.score or 0),
    ])


def _candidate(label, risk, reason, obj):
    return {
        'label': label,
        'risk': risk,
        'reason': reason,
        'object': obj,
    }


def _same_date_filter(field_name, date_value):
    if not date_value:
        return Q()
    return Q(**{'%s__year' % field_name: date_value.year, '%s__month' % field_name: date_value.month, '%s__day' % field_name: date_value.day})


def _business_number_candidates(application):
    if not application.work_num:
        return []

    candidates = []
    if application.work_type == 'orders':
        from orders.models import Orders
        for obj in Orders.objects.filter(orders_num=application.work_num):
            candidates.append(_candidate('工单', 'high', '编号已存在：%s' % application.work_num, obj))
    elif application.work_type == 'cutovers':
        from cutovers.models import Cutovers
        for obj in Cutovers.objects.filter(cutover_num=application.work_num):
            candidates.append(_candidate('割接', 'high', '编号已存在：%s' % application.work_num, obj))
    return candidates


def _business_title_candidates(application):
    date_value = normalized_work_date(application)
    normalized = normalize_title(application.title)
    if not normalized or not date_value:
        return []

    candidates = []
    model_configs = []
    if application.work_type == 'orders':
        from orders.models import Orders
        model_configs.append((Orders, '工单', 'deadline_at'))
    elif application.work_type == 'cutovers':
        from cutovers.models import Cutovers
        model_configs.append((Cutovers, '割接', 'deadline_at'))
    elif application.work_type == 'posts':
        from posts.models import Posts
        model_configs.append((Posts, '项目', 'deadline_at'))
    elif application.work_type == 'routine':
        from routine.models import Routine
        model_configs.append((Routine, '日常工作', 'created_at'))
    elif application.work_type == 'faulty':
        from faulty.models import Faulty
        model_configs.append((Faulty, '故障处理', 'created_at'))
    elif application.work_type == 'bonuses':
        from bonuses.models import Bonuses
        model_configs.append((Bonuses, '特殊加分', 'created_at'))

    for model_cls, label, date_field in model_configs:
        query = model_cls.objects.filter(_same_date_filter(date_field, date_value))
        for obj in query:
            if normalize_title(getattr(obj, 'title', '')) == normalized:
                candidates.append(_candidate(label, 'medium', '同日期标题相同', obj))
    return candidates


def _application_candidates(application):
    from accounts.models import WorkApplication

    date_value = normalized_work_date(application)
    normalized = normalize_title(application.title)
    query = WorkApplication.objects.filter(work_type=application.work_type)
    if application.pk:
        query = query.exclude(pk=application.pk)

    candidates = []
    if application.work_num:
        for obj in query.filter(work_num=application.work_num).exclude(work_num=''):
            candidates.append(_candidate('工作量申请', 'high', '已有相同编号申请', obj))

    for obj in query:
        obj_date = normalized_work_date(obj)
        if normalized and obj_date == date_value and normalize_title(obj.title) == normalized:
            candidates.append(_candidate('工作量申请', 'medium', '同日期标题相同', obj))
        if (
            obj.applicant_id == application.applicant_id and
            obj_date == date_value and
            float(obj.score or 0) == float(application.score or 0)
        ):
            candidates.append(_candidate('工作量申请', 'medium', '同申请人同日期同分数', obj))
    return candidates


def find_duplicate_candidates(application):
    candidates = []
    candidates.extend(_application_candidates(application))
    candidates.extend(_business_number_candidates(application))
    candidates.extend(_business_title_candidates(application))
    return candidates


def update_duplicate_status(application):
    candidates = find_duplicate_candidates(application)
    application.duplicate_signature = build_duplicate_signature(application)
    application.duplicate_checked_at = timezone.now()
    if candidates:
        application.duplicate_status = 'suspected'
    elif application.duplicate_status not in ('overridden', 'confirmed_duplicate'):
        application.duplicate_status = 'none'
    application.save(update_fields=[
        'duplicate_status',
        'duplicate_signature',
        'duplicate_checked_at',
    ])
    return candidates


def approval_requires_duplicate_override(application):
    return application.duplicate_status == 'suspected'
