from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from scores.models import *
from posts.models import Posts
from cutovers.models import Cutovers
from orders.models import Orders
from bonuses.models import Bonuses
from routine.models import Routine
from faulty.models import Faulty
from templates.constant_files import *#scoreOfAllWorkers,POST_SCORE_FLAG,CUTOVER_SCORE_FLAG,ORDERS_SCORE_FLAG,BONUSES_SCORE_FLAG,FAULTY_SCORE_FLAG,ROUTINE_SCORE_FLAG
from templates.forms import AttitudeForm, DisciplineForm,ResponsibilityForm
import math
import datetime
from django.db.models import Avg


thisSeason = MONTH_LIST[0]
thisYear = datetime.datetime.now().year
thisMonth = datetime.datetime.now().month

# if thisMonth <= 4 :
#     thisSeason = SEASON_LIST[0]
# elif thisMonth <= 7:
#     thisSeason = SEASON_LIST[1]
# elif thisMonth <= 10:
#     thisSeason = SEASON_LIST[2]
# else:
#     thisSeason = SEASON_LIST[3]    

thisSeason = MONTH_LIST[thisMonth-1]
thisSeasonStr = str(thisYear)+'年'+str(thisSeason)

if thisMonth == 1:
    thisSeasonStr = str(thisYear-1)+'年十二月'

print(thisSeasonStr)

def democracy(request):
    
    democracy_form = {'attitude_form':0,'descipline_form':0,'responsibility_form':0}

    id = request.user.id
    print(id)
    if id is None: 
        return redirect('dashboard')

    user_basic = User.objects.get(id=id)
        
     #get all types of work info
    myName = str(user_basic.last_name+user_basic.first_name)
    is_attitude_exist_flag = Attitude.objects.all().filter(worker_name=myName, year_season= thisSeasonStr)
    is_dis_exist_flag = Discipline.objects.all().filter(worker_name=myName, year_season= thisSeasonStr)
    is_responsibility_exist_flag = Responsibility.objects.all().filter(worker_name=myName, year_season= thisSeasonStr)
    if  is_attitude_exist_flag  or  is_dis_exist_flag  or  is_responsibility_exist_flag :
        print('objects  exists')
        return redirect('dashboard')

    if request.method == 'POST':

        attitude_form = AttitudeForm(request.POST)
        descipline_form = DisciplineForm(request.POST)
        reponsibility_form = ResponsibilityForm(request.POST)
        if attitude_form.is_valid() and descipline_form.is_valid() and reponsibility_form.is_valid():
            at = attitude_form.save(commit=False)
            de = descipline_form.save(commit=False)
            re = reponsibility_form.save(commit=False)

            at.worker_name = myName
            at.year_season = thisSeasonStr
            de.worker_name = myName
            de.year_season = thisSeasonStr
            re.worker_name = myName
            re.year_season = thisSeasonStr

            at.save()
            de.save()
            re.save()
            return redirect('success')

        else:
            print('invalid data')


        

    else:
        attitude_form = AttitudeForm()
        descipline_form = DisciplineForm()
        reponsibility_form = ResponsibilityForm()

    democracy_form['attitude_form'] = attitude_form
    democracy_form['descipline_form'] = descipline_form
    democracy_form['reponsibility_form'] = reponsibility_form

    context = {
        'democracy':democracy_form,
        'title': '民主测评',
    }    
    return render(request, 'scores/democracy.html', context)

def success(request):
     return render(request, 'scores/success.html')

# show tables of workers' scores
def index(request):
    # return HttpResponse('hello django')

    scores = Scores.objects.all().filter(
        score_year_month__contains='2021',worker_name__in=['张晨','常晓波','陈立栋','黄锵栩','汪志武','韦国锐','苏飓','霍晓歌','李晓昕','郭少钏','于秋思','苏伟衡','杨晓','刘峰','刘江','刘雷',])  # the final scores of a month

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
        sumScore['sum_routine'] = round(score.score_routine, 2)
        sumScore['sum_faulty'] = round(score.score_faulty, 2)
        sumScore['sum_all'] = round(
            score.score_posts + score.score_cutovers + score.score_orders + score.score_bonuses + score.score_routine + score.score_faulty, 2)
        #print(sumScore['sum_all'])
        sumScores[i] = sumScore
        i += 1


    updateScoreOfWorkers(2021, 2)
    # print(scoreOfAllWorkers)
    #updateScoreOfWorkers(2020, 11)
    # print(scoreOfAllWorkers)
    #updateScoreOfWorkers(2020, 12)
    # print(scoreOfAllWorkers)
    # print(sumScores)

    #season4 = getJixiaoByGroups()

    season4 = getJixiaoByItemsLimit()
    #season4 = None
    getDemocacyScore(thisSeasonStr)
    sortedPerformance = sorted(JIXIAO.items(), key=lambda x: x[1][2], reverse=True)
    print(sortedPerformance)

    visitorIp = visitor_ip_address(request)
    context = {
        'title': '分数',
        'scores': scores,
        'sumScores': sumScores,
        'season4': season4,
        'jixiao': sortedPerformance,
        'visitorIp':visitorIp,
        'thisSeasonStr':thisSeasonStr,

    }
    
    return render(request, 'scores/index.html', context)


def getDemocacyScore(thisSeasonStr):
    print('--->'+thisSeasonStr+'<---')
    global JIXIAO
    
    for worker_name, work_name_interpreter in NAME_INTERPRETER.items():
        
        work_name_item_at = 'at_'+ work_name_interpreter
        attitude_average = Attitude.objects.all().filter(year_season = thisSeasonStr).aggregate(Avg(work_name_item_at))
        work_name_item_re = 're_'+ work_name_interpreter
        reponsi_average = Responsibility.objects.all().filter(year_season = thisSeasonStr).aggregate(Avg(work_name_item_re))
        work_name_item_di = 'di_'+ work_name_interpreter
        disci_average = Discipline.objects.all().filter(year_season = thisSeasonStr).aggregate(Avg(work_name_item_di))

        attitude_score = 0
        responsibility_score = 0
        discipline_score = 0

        if(attitude_average and attitude_average[work_name_item_at+'__avg']):
            attitude_score = attitude_average[work_name_item_at+'__avg']*5/100
        if(reponsi_average and reponsi_average[work_name_item_re+'__avg']):
            responsibility_score = reponsi_average[work_name_item_re+'__avg']*5/100
        if(disci_average and disci_average[work_name_item_di+'__avg']):
            discipline_score = disci_average[work_name_item_di+'__avg']*5/100

        JIXIAO[worker_name][0] = attitude_score + responsibility_score + discipline_score
        JIXIAO[worker_name][2] = JIXIAO[worker_name][0] + JIXIAO[worker_name][1]

    return



# ################
# group algorithm
# ################
def getJixiaoByGroups():
#s4 means forth season 
    season4 = Scores.objects.raw('''select name as id,round((a+b+c+d+e+f),2) s4
    from (
    SELECT worker_name name,sum(score_posts) a,sum(score_orders) b, sum(score_cutovers) c, sum(score_bonuses) d,
    sum(score_faulty) e, sum(score_routine)/10 f  
    from scores_scores
    where score_year_month in('2020-1','2020-2','2020-3') and  
    worker_name in('张晨','常晓波','陈立栋','韦国锐','黄锵栩','汪志武','苏飓','霍晓歌','李晓昕','郭少钏','于秋思','苏伟衡','杨晓','刘峰','刘江','刘雷')
    GROUP BY worker_name
    ) AS SEASON4
    ORDER BY s4 desc''')

    wlwAll = 0
    othersAll = 0
    gongzhongAll = 0
    shutongAll = 0

    for s in season4:
        if(s.id=='刘雷'):
            wlwAll +=s.s4
        if(s.id=='刘峰'):
            wlwAll +=s.s4
        if(s.id=='刘江'):
            wlwAll +=s.s4
        if(s.id=='杨晓'):
            wlwAll +=s.s4
        if(s.id=='张晨'):
           othersAll +=s.s4
        if(s.id=='李晓昕'):
            othersAll +=s.s4  
        if(s.id=='郭少钏'):
            othersAll +=s.s4   
        if(s.id=='苏飓'):
            othersAll +=s.s4  
        if(s.id=='霍晓歌'):
            othersAll +=s.s4  
        if(s.id=='陈立栋'):
            othersAll +=s.s4  
        if(s.id=='于秋思'):
            othersAll +=s.s4  
        if(s.id=='常晓波'):
           othersAll +=s.s4
        if(s.id=='苏伟衡'):
            othersAll +=s.s4   


   # WlwAll = season4['刘雷']+ season4['刘峰']+season4['刘江']
   # OthersAll = season4['杨晓']+season4['张晨']+season4['李晓昕']+season4['郭少钏']+season4['苏伟衡']+season4['苏飓']+season4['陈立栋']+season4['于秋思']+season4['霍晓歌']+season4['常晓波']
    
    averageAll = (wlwAll+othersAll) / (WLW_NUMBERS+OTHERS_NUMBERS)
    averageWlw = (wlwAll)/WLW_NUMBERS
    averageGongzhong = (gongzhongAll)/GONGZHONG_NUMBERS
    averageShutTong = (shutongAll)/SHUTONG_NUMBERS
    averageOthers = (othersAll)/OTHERS_NUMBERS
    if (averageAll == 0):
        averageAll = 1
    for s in season4:
        if(s.id=='刘雷'):
            JIXIAO['刘雷'][1] = round((s.s4-(averageWlw-averageAll))/averageAll,2)
            JIXIAO['刘雷'][0] = s.s4
        if(s.id=='刘峰'):
            JIXIAO['刘峰'][1] = round((s.s4-(averageWlw-averageAll))/averageAll,2)
            JIXIAO['刘峰'][0] = s.s4
        if(s.id=='刘江'):
            JIXIAO['刘江'][1] = round((s.s4-(averageWlw-averageAll))/averageAll,2)
            JIXIAO['刘江'][0] = s.s4
        if(s.id=='杨晓'):
            JIXIAO['杨晓'][1] = round((s.s4-(averageWlw-averageAll))/averageAll,2)
            JIXIAO['杨晓'][0] = s.s4
        # if(s.id=='张晨'):
        #     JIXIAO['张晨'][1] = round((s.s4-(averageOthers-averageAll))/averageAll,2)
        #     JIXIAO['张晨'][0] = s.s4
        if(s.id=='李晓昕'):
            JIXIAO['李晓昕'][1] = round((s.s4-(averageOthers-averageAll))/averageAll,2)  
            JIXIAO['李晓昕'][0] = s.s4
        if(s.id=='郭少钏'):
            JIXIAO['郭少钏'][1] = round((s.s4-(averageOthers-averageAll))/averageAll ,2)
            JIXIAO['郭少钏'][0] = s.s4
        if(s.id=='苏飓'):
            JIXIAO['苏飓'][1] = round((s.s4-(averageOthers-averageAll))/averageAll ,2)
            JIXIAO['苏飓'][0] = s.s4
        if(s.id=='霍晓歌'):
            JIXIAO['霍晓歌'][1] = round((s.s4-(averageOthers-averageAll))/averageAll,2) 
            JIXIAO['霍晓歌'][0] = s.s4
        # if(s.id=='陈立栋'):
        #     JIXIAO['陈立栋'][1] = round((s.s4-(averageOthers-averageAll))/averageAll,2)  
        #     JIXIAO['陈立栋'][0] = s.s4
        if(s.id=='苏伟衡'):
            JIXIAO['苏伟衡'][1] = round((s.s4-(averageOthers-averageAll))/averageAll,2)
            JIXIAO['苏伟衡'][0] = s.s4
        if(s.id=='于秋思'):
            JIXIAO['于秋思'][1] = round((s.s4-(averageOthers-averageAll))/averageAll,2)
            JIXIAO['于秋思'][0] = s.s4
        # if(s.id=='常晓波'):
        #     JIXIAO['常晓波'][1] = round((s.s4-(averageOthers-averageAll))/averageAll ,2)
        #     JIXIAO['常晓波'][0] = s.s4       

    return season4


#
# calculate items
#
def getJixiaoByItemsLimit():
    global JIXIAO

    season4 = Scores.objects.raw('''SELECT worker_name as id,sum(score_posts) postScores,sum(score_orders) orderScores,
	sum(score_cutovers) cutoverScores, sum(score_bonuses) bonuseScores, sum(score_faulty) faultyScores, sum(score_routine) routineScores  
    from scores_scores
    where score_year_month in('2021-2') and  
    worker_name in('张晨','常晓波','陈立栋','韦国锐','黄锵栩','汪志武','苏飓','霍晓歌','李晓昕','郭少钏','于秋思','苏伟衡','杨晓','刘峰','刘江','刘雷')
    GROUP BY worker_name
''')



    for s in season4:
        print(s.id)
        for worker_name in NAMES:
            if(s.id == worker_name):
                JIXIAO[worker_name][1] = getJixiao(s.postScores, s.orderScores, s.cutoverScores, s.bonuseScores, s.faultyScores, s.routineScores)
               

    return season4


def getJixiao(postScores, orderScores, cutoverScores, bonusScores, faultyScores, routineScores):
    
    p = POST_SHARE * (1 - math.exp(-1 * POST_LAMADA * postScores)) 
    o = ORDER_SHARE * (1 - math.exp(-1 * ORDER_LAMADA * orderScores)) 
    c = CUTOVER_SHARE * (1 - math.exp(-1 * CUTOVER_LAMADA * cutoverScores)) 
    b = bonusScores #BONUS_SHARE * (1 - math.exp(-1 * BONUS_LAMADA * bonusScores)) 
    f = FAULTY_SHARE * (1 - math.exp(-1 * FAULTY_LAMADA * faultyScores)) 
    r = ROUTINE_SHARE * (1 - math.exp(-1 * ROUTINE_LAMADA * routineScores)) 
    percentage_of_score = round(p+o+c+b+f+r,4)

    return percentage_of_score

# update wokers scores

def updateScoreOfWorkers(myYear, myMonth):
    global scoreOfAllWorkers

    global POST_SCORE_FLAG
    global CUTOVER_SCORE_FLAG
    global ORDERS_SCORE_FLAG
    global BONUSES_SCORE_FLAG
    global FAULTY_SCORE_FLAG
    global ROUTINE_SCORE_FLAG
    # set scoreOfAllWorkers to 0
    initScoreOfAllWorkers()

    try:
        posts = Posts.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        print(posts)
        cutovers = Cutovers.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        print(cutovers)
        orders = Orders.objects.filter(
            deadline_at__year=myYear, deadline_at__month=myMonth)
        print(orders)
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
        print('print faulty except complaints',faulty)
        countScores(faulty, FAULTY_SCORE_FLAG)
    if routine is not None:
        countScores(routine, ROUTINE_SCORE_FLAG)

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
        print('this is score',myScore.pj_leader)
        if flag != CUTOVER_SCORE_FLAG:
            if myScore.is_not_delayed and myScore.body !='':
                print('not delayed')
                pj_leader_score = round(
                    myScore.workload_allot * myScore.pj_score, 2)
                pj_participant1_score = round(
                    myScore.workload_allot1 * myScore.pj_score, 2)
                pj_participant2_score = round(
                    myScore.workload_allot2 * myScore.pj_score, 2)
                pj_participant3_score = round(
                    myScore.workload_allot3 * myScore.pj_score, 2)


                if flag == POST_SCORE_FLAG and 1 == myScore.pj_progress:
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
                    # print(pj_leader_score)
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

                if flag == ROUTINE_SCORE_FLAG:
                    if myScore.pj_leader != '':
                        scoreOfAllWorkers[myScore.pj_leader]['routine'] += pj_leader_score
                    if myScore.pj_participant1 != '':
                        scoreOfAllWorkers[myScore.pj_participant1]['routine'] += pj_participant1_score
                    if myScore.pj_participant2 != '':
                        scoreOfAllWorkers[myScore.pj_participant2]['routine'] += pj_participant2_score
                    if myScore.pj_participant3 != '':
                        scoreOfAllWorkers[myScore.pj_participant3]['routine'] += pj_participant3_score

                if flag == FAULTY_SCORE_FLAG:
                    if myScore.pj_leader != '':
                        scoreOfAllWorkers[myScore.pj_leader]['faulty'] += pj_leader_score
                    if myScore.pj_participant1 != '':
                        scoreOfAllWorkers[myScore.pj_participant1]['faulty'] += pj_participant1_score
                    if myScore.pj_participant2 != '':
                        scoreOfAllWorkers[myScore.pj_participant2]['faulty'] += pj_participant2_score
                    if myScore.pj_participant3 != '':
                        scoreOfAllWorkers[myScore.pj_participant3]['faulty'] += pj_participant3_score
        else:
            pj_leader_score = 3 #score for per cutover
            if myScore.pj_leader != '' and myScore.is_not_delayed and myScore.body !='':
                scoreOfAllWorkers[myScore.pj_leader]['cutovers'] += pj_leader_score
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
