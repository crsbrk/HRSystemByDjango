import datetime

from django.conf import settings
from django.utils import timezone

from accounts.workers import worker_display_name
from templates.constant_files import FAULTY_TYPES, MANUFA_TYPES, ORDER_TYPES


def application_score_period(application):
    period = application.work_date
    if period is None and application.created_at:
        period = application.created_at.date()
    if period is None:
        period = timezone.localdate()
    return period.year, period.month


def application_work_datetime(application):
    period = application.work_date
    if period is None and application.created_at:
        period = application.created_at.date()
    if period is None:
        period = timezone.localdate()

    work_datetime = datetime.datetime.combine(period, datetime.time.min)
    if settings.USE_TZ and timezone.is_naive(work_datetime):
        return timezone.make_aware(work_datetime, timezone.get_current_timezone())
    return work_datetime


def valid_choice_or_default(value, choices, default):
    valid_values = {item[0] for item in choices}
    return value if value in valid_values else default


def common_people_data(application):
    return {
        'pj_leader': worker_display_name(application.applicant),
        'workload_allot': application.workload_allot,
        'pj_participant1': application.pj_participant1,
        'workload_allot1': application.workload_allot1,
        'pj_participant2': application.pj_participant2,
        'workload_allot2': application.workload_allot2,
        'pj_participant3': application.pj_participant3,
        'workload_allot3': application.workload_allot3,
    }


def materialized_payload(application):
    from bonuses.models import Bonuses
    from cutovers.models import Cutovers
    from faulty.models import Faulty
    from orders.models import Orders
    from posts.models import Posts
    from routine.models import Routine

    work_datetime = application_work_datetime(application)
    body = application.description or application.review_comment or '由工作量申请审批生成'
    score = application.score

    if application.work_type == 'orders':
        payload = common_people_data(application)
        payload.update({
            'orders_num': application.work_num or 'APP-%s' % application.pk,
            'title': application.title,
            'pj_score': score,
            'orders_type': valid_choice_or_default(application.work_subtype, ORDER_TYPES, '其他'),
            'deadline_at': work_datetime,
            'created_at': work_datetime,
            'is_not_delayed': True,
            'is_finished': True,
            'body': body,
        })
        return Orders, payload

    if application.work_type == 'cutovers':
        return Cutovers, {
            'cutover_num': application.work_num or 'APP-%s' % application.pk,
            'title': application.title,
            'pj_leader': worker_display_name(application.applicant),
            'deadline_at': work_datetime,
            'is_not_delayed': True,
            'body': body,
        }

    if application.work_type == 'posts':
        payload = common_people_data(application)
        payload.update({
            'title': application.title,
            'pj_score': score,
            'deadline_at': work_datetime,
            'pj_progress': application.work_progress if application.work_progress is not None else 1,
            'is_not_delayed': True,
            'created_at': work_datetime,
            'body': body,
        })
        return Posts, payload

    if application.work_type == 'routine':
        payload = common_people_data(application)
        payload.update({
            'title': application.title,
            'pj_score': score,
            'is_not_delayed': True,
            'created_at': work_datetime,
            'body': body,
        })
        return Routine, payload

    if application.work_type == 'faulty':
        payload = common_people_data(application)
        payload.update({
            'title': application.title,
            'pj_score': score,
            'pj_type': valid_choice_or_default(application.work_subtype, FAULTY_TYPES, '其他'),
            'pj_manufacturer': valid_choice_or_default(application.work_manufacturer, MANUFA_TYPES, '其他'),
            'is_not_delayed': True,
            'created_at': work_datetime,
            'body': body,
        })
        return Faulty, payload

    if application.work_type == 'bonuses':
        payload = common_people_data(application)
        payload.update({
            'title': application.title,
            'pj_score': score,
            'is_not_delayed': True,
            'created_at': work_datetime,
            'body': body,
        })
        return Bonuses, payload

    raise ValueError('Unsupported work application type: %s' % application.work_type)


def sync_application_work_item(application):
    model_cls, payload = materialized_payload(application)
    obj = None
    if application.materialized_model == application.work_type and application.materialized_object_id:
        obj = model_cls.objects.filter(pk=application.materialized_object_id).first()

    if obj is None:
        obj = model_cls()

    for field_name, value in payload.items():
        setattr(obj, field_name, value)
    obj.save()

    update_fields = []
    if application.materialized_model != application.work_type:
        application.materialized_model = application.work_type
        update_fields.append('materialized_model')
    if application.materialized_object_id != obj.pk:
        application.materialized_object_id = obj.pk
        update_fields.append('materialized_object_id')
    if update_fields:
        application.save(update_fields=update_fields)
    return obj


def delete_application_work_item(application):
    if not application.materialized_model or not application.materialized_object_id:
        return

    model_cls, _ = materialized_payload(application)
    model_cls.objects.filter(pk=application.materialized_object_id).delete()
    application.materialized_model = ''
    application.materialized_object_id = None
    application.save(update_fields=['materialized_model', 'materialized_object_id'])


def refresh_scores_for_application(application):
    """Recalculate the Scores row touched by an approved work application."""
    from scores.views import collect_worker_names, get_worker_profiles, updateScoreOfWorkers

    year, month = application_score_period(application)
    worker_profiles = get_worker_profiles()
    worker_names = collect_worker_names(worker_profiles)
    applicant_name = worker_display_name(application.applicant)
    if applicant_name and applicant_name not in worker_names:
        worker_names.append(applicant_name)

    updateScoreOfWorkers(year, month, sorted(worker_names))
    return year, month
