from django.shortcuts import render
from scores.models import Scores
from posts.models import Posts
from cutovers.models import Cutovers
from orders.models import Orders
from bonuses.models import Bonuses
from django.db.models import Sum

POST_SCORE_FLAG = 1
CUTOVER_SCORE_FLAG = 2
ORDERS_SCORE_FLAG = 3
BONUSES_SCORE_FLAG = 4

scoreOfAllWorkers = {
    '陈立栋': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '常晓波': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '刘江': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '刘雷': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '刘峰': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '冯庆': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '郭少钏': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '于秋思': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '苏飓': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '苏伟衡': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '杨晓': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '霍晓歌': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '李晓昕': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '韦国锐': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
    '张晨': {'posts': 0, 'orders': 0, 'cutovers': 0, 'bonuses': 0},
}


# show tables of workers' scores
def index(request):
    # return HttpResponse('hello django')

    scores = Scores.objects.all().filter(
        score_year_month__contains='2018')  # the final scores of a month

    i = 0
    sumScores = {}

    for score in scores:
        sumScore = {}
        sumScore['sum_name'] = score.worker_name
        sumScore['sum_month'] = score.score_year_month
        sumScore['sum_posts'] = round(score.score_posts, 2)
        sumScore['sum_cutovers'] = round(score.score_cutovers, 2)
        sumScore['sum_orders'] = round(score.score_orders, 2)
        sumScore['sum_bonuses'] = round(score.score_bonuses, 2)
        sumScore['sum_all'] = round(
            score.score_posts + score.score_cutovers + score.score_orders + score.score_bonuses, 2)
        sumScores[i] = sumScore
        i += 1

    season4 = Scores.objects.raw('''select name as id,round((a+b+c+d),2) s4
from (
SELECT worker_name name,sum(score_posts) a,sum(score_orders) b, sum(score_cutovers) c, sum(score_bonuses) d
from scores_scores
where score_year_month in('2018-11','2018-10','2018-12')
GROUP BY worker_name
) AS SEASON4
ORDER BY s4 desc''')
    updateScoreOfWorkers(2018, 10)
    # print(scoreOfAllWorkers)
    updateScoreOfWorkers(2018, 11)
    # print(scoreOfAllWorkers)
    updateScoreOfWorkers(2018, 12)
    # print(scoreOfAllWorkers)
    # print(sumScores)
    context = {
        'title': '分数',
        'scores': scores,
        'sumScores': sumScores,
        'season4': season4

    }

    return render(request, 'scores/index.html', context)

# update wokers scores


def updateScoreOfWorkers(myYear, myMonth):
    global scoreOfAllWorkers

    global POST_SCORE_FLAG
    global CUTOVER_SCORE_FLAG
    global ORDERS_SCORE_FLAG
    global BONUSES_SCORE_FLAG

    # set scoreOfAllWorkers to 0
    initScoreOfAllWorkers()

    try:
        posts = Posts.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        cutovers = Cutovers.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        orders = Orders.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        bonuses = Bonuses.objects.filter(
            created_at__year=myYear, created_at__month=myMonth)

    except Posts.DoesNotExist:
        posts = None
    except Cutovers.DoesNotExist:
        cutovers = None
    except Orders.DoesNotExist:
        orders = None
    except Bonuses.DoesNotExist:
        bonuses = None

    if posts is not None:
        countScores(posts, POST_SCORE_FLAG)
    if orders is not None:
        #print("orders is not none")
        countScores(orders, ORDERS_SCORE_FLAG)
    if bonuses is not None:
        countScores(bonuses, BONUSES_SCORE_FLAG)
    if cutovers is not None:
        countScores(cutovers, CUTOVER_SCORE_FLAG)

    # print(scoreOfAllWorkers)

    for aWorker in scoreOfAllWorkers:
        try:

            obj = Scores.objects.get(
                worker_name=aWorker, score_year_month=str(myYear) + '-' + str(myMonth))
            obj.score_posts = scoreOfAllWorkers[aWorker]['posts']
            obj.score_orders = scoreOfAllWorkers[aWorker]['orders']
            obj.score_cutovers = scoreOfAllWorkers[aWorker]['cutovers']
            obj.score_bonuses = scoreOfAllWorkers[aWorker]['bonuses']
            obj.save()
        except Scores.DoesNotExist:
            obj = Scores(worker_name=aWorker,
                         score_posts=scoreOfAllWorkers[aWorker]['posts'],
                         score_orders=scoreOfAllWorkers[aWorker]['orders'],
                         score_cutovers=scoreOfAllWorkers[aWorker]['cutovers'],
                         score_bonuses=scoreOfAllWorkers[aWorker]['bonuses'],
                         score_year_month=str(myYear) + '-' + str(myMonth))
            obj.save()

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

    for myScore in myScores:
        # count the socre of each worker
        #print('this is score',myScore.pj_leader)
        if flag != CUTOVER_SCORE_FLAG:
            pj_leader_score = round(
                myScore.workload_allot * myScore.pj_score, 2)
            pj_participant1_score = round(
                myScore.workload_allot1 * myScore.pj_score, 2)
            pj_participant2_score = round(
                myScore.workload_allot2 * myScore.pj_score, 2)
            pj_participant3_score = round(
                myScore.workload_allot3 * myScore.pj_score, 2)

            if flag == POST_SCORE_FLAG:
                if myScore.pj_leader != '':
                    scoreOfAllWorkers[myScore.pj_leader]['posts'] += pj_leader_score
                if myScore.pj_participant1 != '':
                    scoreOfAllWorkers[myScore.pj_participant1]['posts'] += pj_participant1_score
                if myScore.pj_participant2 != '':
                    scoreOfAllWorkers[myScore.pj_participant2]['posts'] += pj_participant2_score
                if myScore.pj_participant3 != '':
                    scoreOfAllWorkers[myScore.pj_participant3]['posts'] += pj_participant3_score

            if flag == ORDERS_SCORE_FLAG:
                #print("this is orders socre flag")
                #print(pj_leader_score)
                if myScore.pj_leader != '':
                    scoreOfAllWorkers[myScore.pj_leader]['orders'] += pj_leader_score
                if myScore.pj_participant1 != '':
                    scoreOfAllWorkers[myScore.pj_participant1]['orders'] += pj_participant1_score
                if myScore.pj_participant2 != '':
                    scoreOfAllWorkers[myScore.pj_participant2]['orders'] += pj_participant2_score
                if myScore.pj_participant3 != '':
                    scoreOfAllWorkers[myScore.pj_participant3]['orders'] += pj_participant3_score

            if flag == BONUSES_SCORE_FLAG:
                if myScore.pj_leader != '':
                    scoreOfAllWorkers[myScore.pj_leader]['bonuses'] += pj_leader_score
                if myScore.pj_participant1 != '':
                    scoreOfAllWorkers[myScore.pj_participant1]['bonuses'] += pj_participant1_score
                if myScore.pj_participant2 != '':
                    scoreOfAllWorkers[myScore.pj_participant2]['bonuses'] += pj_participant2_score
                if myScore.pj_participant3 != '':
                    scoreOfAllWorkers[myScore.pj_participant3]['bonuses'] += pj_participant3_score
        else:
            pj_leader_score = 3
            if myScore.pj_leader != '':
                scoreOfAllWorkers[myScore.pj_leader]['cutovers'] += pj_leader_score
    return


def initScoreOfAllWorkers():
    global scoreOfAllWorkers
    for k, v in scoreOfAllWorkers.items():
        v['posts'] = 0
        v['cutovers'] = 0
        v['orders'] = 0
        v['bonuses'] = 0
    return
