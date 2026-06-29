import math

from django.contrib.auth.models import User
from django.db.models import Avg

from accounts.workers import worker_display_name
from scores.models import (
    SCORE_CATEGORY_CHOICES,
    DemocracyRating,
    ScoreFormulaPolicy,
    ScoreRankingSnapshot,
    Scores,
)
from templates.constant_files import MONTH_LIST


CATEGORY_KEYS = tuple(choice[0] for choice in SCORE_CATEGORY_CHOICES)


def get_or_create_default_policy():
    policy, _ = ScoreFormulaPolicy.objects.get_or_create(
        name='当前兼容公式',
        effective_year=2000,
        effective_month=1,
        defaults={
            'ranking_formula': 'legacy_cap40',
            'is_active': True,
            'notes': '系统默认兼容公式：项目和特殊加分不压缩，工单/割接/故障/日常合计封顶40。',
        },
    )
    return policy


def get_policy_for_period(year, month):
    policy = (
        ScoreFormulaPolicy.objects
        .filter(is_active=True)
        .filter(
            effective_year__lt=year,
        )
        .order_by('-effective_year', '-effective_month', '-updated_at')
        .first()
    )
    same_year_policy = (
        ScoreFormulaPolicy.objects
        .filter(is_active=True, effective_year=year, effective_month__lte=month)
        .order_by('-effective_month', '-updated_at')
        .first()
    )
    if same_year_policy and (
        policy is None or
        (same_year_policy.effective_year, same_year_policy.effective_month) >=
        (policy.effective_year, policy.effective_month)
    ):
        return same_year_policy
    return policy or get_or_create_default_policy()


def build_policy_snapshot(policy):
    rules = {}
    for rule in policy.category_rules.all().order_by('category'):
        rules[rule.category] = {
            'algorithm': rule.algorithm,
            'cap': rule.cap,
            'lambda_value': rule.lambda_value,
            'weight': rule.weight,
        }
    return {
        'policy_id': policy.pk,
        'name': policy.name,
        'effective_year': policy.effective_year,
        'effective_month': policy.effective_month,
        'ranking_formula': policy.ranking_formula,
        'rules': rules,
    }


def raw_scores_from_score(score):
    return {
        'posts': score.score_posts,
        'orders': score.score_orders,
        'cutovers': score.score_cutovers,
        'bonuses': score.score_bonuses,
        'faulty': score.score_faulty,
        'routine': score.score_routine,
    }


def normalize_raw_scores(raw_scores):
    return {key: float(raw_scores.get(key) or 0) for key in CATEGORY_KEYS}


def calculate_category_score(raw_score, rule):
    raw_score = float(raw_score or 0)
    weight = float(rule.weight or 0)
    if rule.algorithm == 'hard_cap':
        return min(raw_score, float(rule.cap or 0)) * weight
    if rule.algorithm == 'exponential':
        cap = float(rule.cap or 0)
        lambda_value = float(rule.lambda_value or 0)
        return cap * (1 - math.exp(-1 * lambda_value * raw_score)) * weight
    return raw_score * weight


def default_calculation_result(raw_scores):
    result = {}
    for key, value in raw_scores.items():
        result['final_%s' % key] = value
    return result


def calculate_work_score(raw_scores, policy):
    raw_scores = normalize_raw_scores(raw_scores)
    result = default_calculation_result(raw_scores)

    if policy.ranking_formula == 'raw_sum':
        result['work_score'] = sum(raw_scores.values())
        return result

    if policy.ranking_formula == 'compressed_sum':
        rules_by_category = {
            rule.category: rule
            for rule in policy.category_rules.all()
        }
        work_score = 0
        for category in CATEGORY_KEYS:
            rule = rules_by_category.get(category)
            final_score = calculate_category_score(raw_scores[category], rule) if rule else raw_scores[category]
            result['final_%s' % category] = final_score
            work_score += final_score
        result['work_score'] = work_score
        return result

    ocfr_score = (
        raw_scores['orders'] +
        raw_scores['cutovers'] +
        raw_scores['faulty'] +
        raw_scores['routine']
    )
    result['work_score'] = min(ocfr_score, 40) + raw_scores['posts'] + raw_scores['bonuses']
    return result


def season_key(year, month):
    return '%s年%s' % (year, MONTH_LIST[month])


def democracy_scores_for_period(year, month):
    rows = (
        DemocracyRating.objects
        .filter(year_season=season_key(year, month))
        .values('target')
        .annotate(
            at_avg=Avg('attitude'),
            re_avg=Avg('responsibility'),
            di_avg=Avg('discipline'),
        )
    )
    target_ids = [row['target'] for row in rows]
    names_by_id = {
        user.id: worker_display_name(user)
        for user in User.objects.filter(id__in=target_ids)
    }

    scores = {}
    for row in rows:
        worker_name = names_by_id.get(row['target'])
        if not worker_name:
            continue
        attitude_score = (row['at_avg'] or 0) * 3.33 / 100
        responsibility_score = (row['re_avg'] or 0) * 3.33 / 100
        discipline_score = (row['di_avg'] or 0) * 3.33 / 100
        scores[worker_name] = attitude_score + responsibility_score + discipline_score
    return scores


def generate_ranking_snapshots(year, month, worker_names=None):
    month_key = '%s-%s' % (year, month)
    scores_query = Scores.objects.filter(score_year_month=month_key)
    if worker_names:
        scores_query = scores_query.filter(worker_name__in=worker_names)

    policy = get_policy_for_period(year, month)
    policy_snapshot = build_policy_snapshot(policy)
    democracy_scores = democracy_scores_for_period(year, month)
    calculated_rows = []

    for score in scores_query.order_by('worker_name'):
        raw_scores = raw_scores_from_score(score)
        calculation = calculate_work_score(raw_scores, policy)
        democracy_score = democracy_scores.get(score.worker_name, 0)
        total_score = calculation['work_score'] + democracy_score
        calculated_rows.append({
            'score': score,
            'raw_scores': raw_scores,
            'calculation': calculation,
            'democracy_score': democracy_score,
            'total_score': total_score,
        })

    calculated_rows.sort(key=lambda row: (-row['total_score'], row['score'].worker_name))
    snapshots = []
    for rank, row in enumerate(calculated_rows, start=1):
        score = row['score']
        raw_scores = row['raw_scores']
        calculation = row['calculation']
        snapshot, _ = ScoreRankingSnapshot.objects.update_or_create(
            worker_name=score.worker_name,
            score_year=year,
            score_month=month,
            defaults={
                'raw_posts': raw_scores['posts'],
                'raw_orders': raw_scores['orders'],
                'raw_cutovers': raw_scores['cutovers'],
                'raw_bonuses': raw_scores['bonuses'],
                'raw_faulty': raw_scores['faulty'],
                'raw_routine': raw_scores['routine'],
                'final_posts': calculation['final_posts'],
                'final_orders': calculation['final_orders'],
                'final_cutovers': calculation['final_cutovers'],
                'final_bonuses': calculation['final_bonuses'],
                'final_faulty': calculation['final_faulty'],
                'final_routine': calculation['final_routine'],
                'work_score': calculation['work_score'],
                'democracy_score': row['democracy_score'],
                'total_score': row['total_score'],
                'rank': rank,
                'policy': policy,
                'policy_snapshot': policy_snapshot,
            },
        )
        snapshots.append(snapshot)

    return snapshots
