from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from scores.models import *
from accounts.models import UserProfileInfo
from posts.models import Posts
from cutovers.models import Cutovers
from orders.models import Orders
from bonuses.models import Bonuses
from routine.models import Routine
from faulty.models import Faulty
from templates.constant_files import *#scoreOfAllWorkers,POST_SCORE_FLAG,CUTOVER_SCORE_FLAG,ORDERS_SCORE_FLAG,BONUSES_SCORE_FLAG,FAULTY_SCORE_FLAG,ROUTINE_SCORE_FLAG
from accounts.workers import worker_display_name, get_worker_names
from scores.services.formulas import generate_ranking_snapshots, get_policy_for_period
import math
import datetime
from django.db.models import Avg, Q
from django.conf import settings


def current_period():
    """返回当前需要统计的（年份, 月份）：排名统计的是上个月；一月回退到上一年十二月。

    必须每次请求时调用，不能在模块导入时计算一次，否则跨月后服务仍用旧日期。
    """
    now = datetime.datetime.now()
    if now.month == 1:
        return now.year - 1, 12
    return now.year, now.month - 1


def get_season_str(year=None, month=None):
    if year is None or month is None:
        year, month = current_period()
    return '%s年%s' % (year, MONTH_LIST[month])

SCORE_FIELDS = ('posts', 'orders', 'cutovers', 'bonuses', 'routine', 'faulty')

# 各员工分数累加桶，按当前注册员工动态重建（不再写死人员名单）
scoreOfAllWorkers = {}


def get_worker_display_name(user):
    name = '%s%s' % (user.last_name, user.first_name)
    return name or user.get_full_name() or user.username


def build_score_bucket(worker_names=None):
    return {
        name: {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0, 'routine': 0, 'faulty': 0}
        for name in (worker_names or [])
        if name
    }


def ensure_worker_score(worker_name):
    if worker_name and worker_name not in scoreOfAllWorkers:
        scoreOfAllWorkers[worker_name] = build_score_bucket([worker_name])[worker_name]


def add_worker_score(worker_name, score_type, amount):
    if not worker_name:
        return
    ensure_worker_score(worker_name)
    scoreOfAllWorkers[worker_name][score_type] += amount


def profile_avatar_url(profile):
    try:
        if profile.profile_pic:
            return profile.profile_pic.url
    except ValueError:
        pass
    return settings.MEDIA_URL + 'profile_pics/selfie.png'


def get_worker_profiles():
    profiles = {}
    for user in User.objects.filter(is_superuser=False).order_by('date_joined', 'id'):
        profile, _ = UserProfileInfo.objects.get_or_create(
            user=user,
            defaults={
                'profile_phone': 0,
                'profile_job_type': '其他',
                'profile_pic': 'profile_pics/selfie.png',
            }
        )
        name = get_worker_display_name(user)
        profiles[name] = {
            'name': name,
            'avatar_url': profile_avatar_url(profile),
            'initials': name[:1] if name else user.username[:1],
            'role': profile.get_role_display(),
            'is_approved': profile.is_approved,
        }
    return profiles


def collect_worker_names(worker_profiles=None):
    worker_names = set((worker_profiles or {}).keys())
    worker_names.update(Scores.objects.exclude(worker_name='').values_list('worker_name', flat=True).distinct())
    for model, fields in (
        (Posts, ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3')),
        (Orders, ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3')),
        (Bonuses, ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3')),
        (Faulty, ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3')),
        (Routine, ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3')),
        (Cutovers, ('pj_leader',)),
    ):
        for field in fields:
            worker_names.update(model.objects.exclude(**{field: ''}).values_list(field, flat=True).distinct())
    return sorted(name for name in worker_names if name)


def worker_meta(worker_name, worker_profiles):
    return worker_profiles.get(worker_name, {
        'name': worker_name,
        'avatar_url': '',
        'initials': worker_name[:1] if worker_name else '-',
        'role': '',
        'is_approved': False,
    })

def democracy(request):
    if not request.user.is_authenticated:
        return redirect('login')

    evaluator = request.user
    thisSeasonStr = get_season_str()

    # 已提交过本季度测评则返回
    already_submitted = DemocracyRating.objects.filter(
        evaluator=evaluator, year_season=thisSeasonStr).exists()
    if already_submitted:
        return redirect('dashboard')

    # 被测评对象 = 所有注册员工（排除超级管理员与自己）
    targets = list(
        User.objects.filter(is_superuser=False)
        .exclude(pk=evaluator.pk)
        .order_by('date_joined', 'id')
    )

    if request.method == 'POST':
        created = 0
        for target in targets:
            def _score(prefix):
                raw = request.POST.get('%s_%s' % (prefix, target.pk))
                try:
                    return int(raw)
                except (TypeError, ValueError):
                    return DEMOCRACY_LIST[0][1]

            DemocracyRating.objects.update_or_create(
                evaluator=evaluator,
                target=target,
                year_season=thisSeasonStr,
                defaults={
                    'attitude': _score('attitude'),
                    'responsibility': _score('responsibility'),
                    'discipline': _score('discipline'),
                },
            )
            created += 1
        return redirect('success')

    target_rows = [{
        'id': target.pk,
        'name': worker_display_name(target),
    } for target in targets]

    context = {
        'title': '民主测评',
        'thisSeasonStr': thisSeasonStr,
        'targets': target_rows,
        'score_choices': DEMOCRACY_LIST,
    }
    return render(request, 'scores/democracy.html', context)

def success(request):
     return render(request, 'scores/success.html')

# show tables of workers' scores
def index(request):
    thisYear, lastMonth = current_period()
    thisSeasonStr = get_season_str(thisYear, lastMonth)

    worker_profiles = get_worker_profiles()
    worker_names = collect_worker_names(worker_profiles)
    updateScoreOfWorkers(thisYear, lastMonth, worker_names)

    scores = Scores.objects.all().filter(
        score_year_month__contains=thisYear, worker_name__in=worker_names).order_by('-score_year_month', 'worker_name')

    i = 0
    sumScores = []

    for score in scores:
        meta = worker_meta(score.worker_name, worker_profiles)
        sumScore = {}
        sumScore['sum_name'] = score.worker_name
        sumScore['avatar_url'] = meta['avatar_url']
        sumScore['initials'] = meta['initials']
        sumScore['sum_month'] = score.score_year_month
        sumScore['sum_posts'] = round(score.score_posts, 2)
        sumScore['sum_cutovers'] = round(score.score_cutovers, 2)
        sumScore['sum_orders'] = round(score.score_orders, 2)
        sumScore['sum_bonuses'] = round(score.score_bonuses, 2)
        sumScore['sum_routine'] = round(score.score_routine, 2)
        sumScore['sum_faulty'] = round(score.score_faulty, 2)
        sumScore['sum_all'] = round(
            score.score_posts + score.score_cutovers + score.score_orders + score.score_bonuses + score.score_routine + score.score_faulty, 2)
        #print(sumScore['sum_all'])
        sumScores.append(sumScore)
        i += 1


    # print(scoreOfAllWorkers)
    #updateScoreOfWorkers(2020, 11)
    # print(scoreOfAllWorkers)
    #updateScoreOfWorkers(2020, 12)
    # print(scoreOfAllWorkers)
    # print(sumScores)

    formula_policy = get_policy_for_period(thisYear, lastMonth)
    generate_ranking_snapshots(thisYear, lastMonth, worker_names)
    ranking_snapshots = ScoreRankingSnapshot.objects.filter(
        score_year=thisYear,
        score_month=lastMonth,
        worker_name__in=worker_names,
    ).order_by('rank', 'worker_name')

    rankingRows = []
    for snapshot in ranking_snapshots:
        worker_name = snapshot.worker_name
        meta = worker_meta(worker_name, worker_profiles)
        rankingRows.append({
            'rank': snapshot.rank,
            'name': worker_name,
            'avatar_url': meta['avatar_url'],
            'initials': meta['initials'],
            'role': meta['role'],
            'is_approved': meta['is_approved'],
            'attitude_score': round(snapshot.democracy_score, 2),
            'work_score': round(snapshot.work_score, 2),
            'total_score': round(snapshot.total_score, 2),
        })

    visitorIp = visitor_ip_address(request)
    context = {
        'title': '分数',
        'scores': scores,
        'sumScores': sumScores,
        'scoreRecordCount': len(sumScores),
        'jixiao': rankingRows,
        'topPerformance': rankingRows[:3],
        'visitorIp':visitorIp,
        'thisSeasonStr':thisSeasonStr,
        'formulaPolicy': formula_policy,

    }
    
    return render(request, 'scores/index.html', context)


def getDemocacyScore(thisSeasonStr, jixiao_scores=None):
    if jixiao_scores is None:
        jixiao_scores = {}

    # 按被测评人聚合本季度三项平均分（动态，支持任意注册员工）
    averages = (
        DemocracyRating.objects
        .filter(year_season=thisSeasonStr)
        .values('target')
        .annotate(
            at_avg=Avg('attitude'),
            re_avg=Avg('responsibility'),
            di_avg=Avg('discipline'),
        )
    )

    target_ids = [row['target'] for row in averages]
    name_by_id = {
        user.id: worker_display_name(user)
        for user in User.objects.filter(id__in=target_ids)
    }

    for row in averages:
        worker_name = name_by_id.get(row['target'])
        if worker_name not in jixiao_scores:
            continue

        attitude_score = (row['at_avg'] or 0) * 3.33 / 100
        responsibility_score = (row['re_avg'] or 0) * 3.33 / 100
        discipline_score = (row['di_avg'] or 0) * 3.33 / 100

        jixiao_scores[worker_name][0] = attitude_score + responsibility_score + discipline_score
        jixiao_scores[worker_name][2] = jixiao_scores[worker_name][0] + jixiao_scores[worker_name][1]

    return jixiao_scores



#
# calculate items
#
def getJixiaoByItemsLimit(worker_names=None, year=None, month=None):
    if year is None or month is None:
        year, month = current_period()
    jixiao_scores = {worker_name: [0, 0, 0] for worker_name in (worker_names or [])}
    month_key = '%s-%s' % (year, month)
    scores = Scores.objects.filter(score_year_month=month_key)
    if worker_names:
        scores = scores.filter(worker_name__in=worker_names)

    for score in scores:
        if score.worker_name not in jixiao_scores:
            jixiao_scores[score.worker_name] = [0, 0, 0]
        work_score = getJixiao(
            score.score_posts,
            score.score_orders,
            score.score_cutovers,
            score.score_bonuses,
            score.score_faulty,
            score.score_routine,
        )
        jixiao_scores[score.worker_name][1] = work_score
        jixiao_scores[score.worker_name][2] = jixiao_scores[score.worker_name][0] + work_score

    return jixiao_scores


###
#change origin scores to new scores
###
def getJixiao2021(postScores, orderScores, cutoverScores, bonusScores, faultyScores, routineScores):
    
    p = POST_SHARE * (1 - math.exp(-1 * POST_LAMADA * postScores)) 
    o = ORDER_SHARE * (1 - math.exp(-1 * ORDER_LAMADA * orderScores)) 
    c = CUTOVER_SHARE * (1 - math.exp(-1 * CUTOVER_LAMADA * cutoverScores)) 
    b = bonusScores #BONUS_SHARE * (1 - math.exp(-1 * BONUS_LAMADA * bonusScores)) 
    f = FAULTY_SHARE * (1 - math.exp(-1 * FAULTY_LAMADA * faultyScores)) 
    r = ROUTINE_SHARE * (1 - math.exp(-1 * ROUTINE_LAMADA * routineScores)) 
    percentage_of_score = round(p+o+c+b+f+r,4)

    return percentage_of_score

def getJixiao(postScores, orderScores, cutoverScores, bonusScores, faultyScores, routineScores):
    
    p = postScores
    o = orderScores
    c = cutoverScores
    b = bonusScores 
    f = faultyScores
    r = routineScores
    
    ocfr = o+c+f+r
    percentage_of_score = ocfr if ocfr <40 else 40

    return percentage_of_score+p+b


# update wokers scores

def updateScoreOfWorkers(myYear, myMonth, worker_names=None):
    global scoreOfAllWorkers

    global POST_SCORE_FLAG
    global CUTOVER_SCORE_FLAG
    global ORDERS_SCORE_FLAG
    global BONUSES_SCORE_FLAG
    global FAULTY_SCORE_FLAG
    global ROUTINE_SCORE_FLAG
    scoreOfAllWorkers = build_score_bucket(worker_names or collect_worker_names())

    try:
        posts = Posts.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        cutovers = Cutovers.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        orders = Orders.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        bonuses = Bonuses.objects.filter(
            created_at__year=myYear, created_at__month=myMonth)
        faulty = Faulty.objects.filter(
            created_at__year=myYear, created_at__month=myMonth).exclude(pj_type='投诉')
        routine = Routine.objects.filter(
            created_at__year=myYear, created_at__month=myMonth)
        

    except Posts.DoesNotExist:
        posts = None
    except Cutovers.DoesNotExist:
        cutovers = None
    except Orders.DoesNotExist:
        orders = None
    except Bonuses.DoesNotExist:
        bonuses = None
    except Faulty.DoesNotExist:
        faulty = None
    except Routine.DoesNotExist:
        routine = None

    if posts is not None:
        countScores(posts, POST_SCORE_FLAG)
    if orders is not None:
        #print("orders is not none")
        countScores(orders, ORDERS_SCORE_FLAG)
    if bonuses is not None:
        countScores(bonuses, BONUSES_SCORE_FLAG)
    if cutovers is not None:
        countScores(cutovers, CUTOVER_SCORE_FLAG)
    if faulty is not None:
        countScores(faulty, FAULTY_SCORE_FLAG)
    if routine is not None:
        countScores(routine, ROUTINE_SCORE_FLAG)

    # 审批通过的工作量申请也计入对应类别（按相关日期/提交日期归属当月）
    addApprovedApplications(myYear, myMonth)

    #    print(scoreOfAllWorkers)

    for aWorker in scoreOfAllWorkers:
        try:
            obj = Scores.objects.get(worker_name=aWorker, score_year_month=str(myYear) + '-' + str(myMonth))
    
            obj.score_posts = scoreOfAllWorkers[aWorker]['posts']
            obj.score_orders = scoreOfAllWorkers[aWorker]['orders']
            obj.score_cutovers = scoreOfAllWorkers[aWorker]['cutovers']
            obj.score_bonuses = scoreOfAllWorkers[aWorker]['bonuses']
            obj.score_faulty = scoreOfAllWorkers[aWorker]['faulty']
            obj.score_routine = scoreOfAllWorkers[aWorker]['routine']
            obj.save()
        except Scores.DoesNotExist:
            obj = Scores(worker_name=aWorker,
                         score_posts=scoreOfAllWorkers[aWorker]['posts'],
                         score_orders=scoreOfAllWorkers[aWorker]['orders'],
                         score_cutovers=scoreOfAllWorkers[aWorker]['cutovers'],
                         score_bonuses=scoreOfAllWorkers[aWorker]['bonuses'],
                         score_routine=scoreOfAllWorkers[aWorker]['routine'],
                         score_faulty=scoreOfAllWorkers[aWorker]['faulty'],
                         score_year_month=str(myYear) + '-' + str(myMonth))
            obj.save()

    return


def addApprovedApplications(myYear, myMonth):
    """把审批通过的工作量申请按类别加入当月分数桶。

    归属月份优先取申请填写的“相关日期”(work_date)，否则取提交日期(created_at)，
    与业务表按日期归月的口径一致。类别(work_type)与 Scores 的六个类别一一对应。
    """
    from accounts.models import WorkApplication

    valid_types = {'posts', 'orders', 'cutovers', 'bonuses', 'routine', 'faulty'}
    fallback_applications = WorkApplication.objects.filter(
        status='approved',
    ).filter(
        Q(materialized_object_id__isnull=True) | Q(materialized_model='')
    ).select_related('applicant')
    for app in fallback_applications:
        period = app.work_date or (app.created_at.date() if app.created_at else None)
        if not period or period.year != myYear or period.month != myMonth:
            continue
        if app.work_type not in valid_types:
            continue
        worker_name = get_worker_display_name(app.applicant)
        add_worker_score(worker_name, app.work_type, app.score)
    return


def outputMyString(outs):
    for o in outs:
        print(o.pj_leader)
    return


def countScores(myScores, flag):
    global scoreOfAllWorkers

    global POST_SCORE_FLAG
    global CUTOVER_SCORE_FLAG
    global ORDERS_SCORE_FLAG
    global BONUSES_SCORE_FLAG
    global ROUTINE_SCORE_FLAG
    global FAULTY_SCORE_FLAG

    for myScore in myScores:
        # count the socre of each worker
        if flag != CUTOVER_SCORE_FLAG:
            if myScore.is_not_delayed and myScore.body !='':
                pj_leader_score = round(
                    myScore.workload_allot * myScore.pj_score, 2)
                pj_participant1_score = round(
                    myScore.workload_allot1 * myScore.pj_score, 2)
                pj_participant2_score = round(
                    myScore.workload_allot2 * myScore.pj_score, 2)
                pj_participant3_score = round(
                    myScore.workload_allot3 * myScore.pj_score, 2)


                if flag == POST_SCORE_FLAG and 1 == myScore.pj_progress:
                    add_worker_score(myScore.pj_leader, 'posts', pj_leader_score)
                    add_worker_score(myScore.pj_participant1, 'posts', pj_participant1_score)
                    add_worker_score(myScore.pj_participant2, 'posts', pj_participant2_score)
                    add_worker_score(myScore.pj_participant3, 'posts', pj_participant3_score)

                if flag == ORDERS_SCORE_FLAG:
                    #print("this is orders socre flag")
                    # print(pj_leader_score)
                    add_worker_score(myScore.pj_leader, 'orders', pj_leader_score)
                    add_worker_score(myScore.pj_participant1, 'orders', pj_participant1_score)
                    add_worker_score(myScore.pj_participant2, 'orders', pj_participant2_score)
                    add_worker_score(myScore.pj_participant3, 'orders', pj_participant3_score)

                if flag == BONUSES_SCORE_FLAG:
                    add_worker_score(myScore.pj_leader, 'bonuses', pj_leader_score)
                    add_worker_score(myScore.pj_participant1, 'bonuses', pj_participant1_score)
                    add_worker_score(myScore.pj_participant2, 'bonuses', pj_participant2_score)
                    add_worker_score(myScore.pj_participant3, 'bonuses', pj_participant3_score)

                if flag == ROUTINE_SCORE_FLAG:
                    add_worker_score(myScore.pj_leader, 'routine', pj_leader_score)
                    add_worker_score(myScore.pj_participant1, 'routine', pj_participant1_score)
                    add_worker_score(myScore.pj_participant2, 'routine', pj_participant2_score)
                    add_worker_score(myScore.pj_participant3, 'routine', pj_participant3_score)

                if flag == FAULTY_SCORE_FLAG:
                    add_worker_score(myScore.pj_leader, 'faulty', pj_leader_score)
                    add_worker_score(myScore.pj_participant1, 'faulty', pj_participant1_score)
                    add_worker_score(myScore.pj_participant2, 'faulty', pj_participant2_score)
                    add_worker_score(myScore.pj_participant3, 'faulty', pj_participant3_score)
        else:
            pj_leader_score = 3 #score for per cutover
            if myScore.pj_leader != '' and myScore.is_not_delayed and myScore.body !='':
                add_worker_score(myScore.pj_leader, 'cutovers', pj_leader_score)
    return


def initScoreOfAllWorkers():
    global scoreOfAllWorkers
    for k, v in scoreOfAllWorkers.items():
        v['posts'] = 0
        v['cutovers'] = 0
        v['orders'] = 0
        v['bonuses'] = 0
        v['faulty'] = 0
        v['routine'] = 0
    return




def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
