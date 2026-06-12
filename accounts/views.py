from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.utils import timezone
from .account_forms import UserForm, UserProfileInfoForm, WorkApplicationForm
from .services import (
  delete_application_work_item,
  refresh_scores_for_application,
  sync_application_work_item,
)
from accounts.models import UserProfileInfo, WorkApplication
from templates.forms import NameForm
from scores.models import Scores
from posts.models import Posts
from cutovers.models import Cutovers
from orders.models import Orders
from bonuses.models import Bonuses
from routine.models import Routine
from faulty.models import Faulty
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q, Sum
from templates.constant_files import ORDER_TYPES, FAULTY_TYPES, MANUFA_TYPES

import datetime


WORK_SUMMARY_CONFIG = (
  {
    'key': 'orders',
    'label': '工单类',
    'icon': 'fas fa-clipboard-list',
    'model': Orders,
    'date_field': 'deadline_at',
    'score_field': 'score_orders',
    'fields': ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3'),
  },
  {
    'key': 'cutovers',
    'label': '割接类',
    'icon': 'fas fa-random',
    'model': Cutovers,
    'date_field': 'deadline_at',
    'score_field': 'score_cutovers',
    'fields': ('pj_leader',),
  },
  {
    'key': 'posts',
    'label': '项目类',
    'icon': 'fas fa-project-diagram',
    'model': Posts,
    'date_field': 'deadline_at',
    'score_field': 'score_posts',
    'fields': ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3'),
  },
  {
    'key': 'routine',
    'label': '日常工作',
    'icon': 'fas fa-tasks',
    'model': Routine,
    'date_field': 'created_at',
    'score_field': 'score_routine',
    'fields': ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3'),
  },
  {
    'key': 'faulty',
    'label': '故障处理',
    'icon': 'fas fa-tools',
    'model': Faulty,
    'date_field': 'created_at',
    'score_field': 'score_faulty',
    'fields': ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3'),
  },
  {
    'key': 'bonuses',
    'label': '特殊加分项',
    'icon': 'fas fa-plus-circle',
    'model': Bonuses,
    'date_field': 'created_at',
    'score_field': 'score_bonuses',
    'fields': ('pj_leader', 'pj_participant1', 'pj_participant2', 'pj_participant3'),
  },
)


def worker_display_name(user):
  name = '%s%s' % (user.last_name, user.first_name)
  return name or user.get_full_name() or user.username


def build_involved_query(worker_name, fields):
  query = Q()
  for field in fields:
    query |= Q(**{field: worker_name})
  return query


def count_involved_work(config, worker_name, year):
  date_lookup = '%s__year' % config['date_field']
  return config['model'].objects.filter(
    build_involved_query(worker_name, config['fields']),
    **{date_lookup: year}
  ).count()


def count_approved_applications(user, work_type, year):
  return WorkApplication.objects.filter(
    applicant=user,
    status='approved',
    work_type=work_type,
    materialized_object_id__isnull=True,
  ).filter(
    Q(work_date__year=year) | Q(work_date__isnull=True, created_at__year=year)
  ).count()


def refresh_dashboard_scores(year):
  from scores.views import collect_worker_names, get_worker_profiles, updateScoreOfWorkers

  now = datetime.datetime.now()
  last_month = now.month if year == now.year else 12
  worker_profiles = get_worker_profiles()
  worker_names = collect_worker_names(worker_profiles)
  for month in range(1, last_month + 1):
    updateScoreOfWorkers(year, month, worker_names)


def build_dashboard_work_summary(user, worker_name, year):
  refresh_dashboard_scores(year)

  score_sums = Scores.objects.filter(
    worker_name=worker_name,
    score_year_month__startswith=str(year),
  ).aggregate(
    score_orders=Sum('score_orders'),
    score_cutovers=Sum('score_cutovers'),
    score_posts=Sum('score_posts'),
    score_routine=Sum('score_routine'),
    score_faulty=Sum('score_faulty'),
    score_bonuses=Sum('score_bonuses'),
  )

  categories = []
  for config in WORK_SUMMARY_CONFIG:
    direct_count = count_involved_work(config, worker_name, year)
    approved_count = count_approved_applications(user, config['key'], year)
    score = round(score_sums.get(config['score_field']) or 0, 2)
    categories.append({
      'key': config['key'],
      'label': config['label'],
      'icon': config['icon'],
      'count': direct_count + approved_count,
      'direct_count': direct_count,
      'approved_count': approved_count,
      'score': score,
      'percent': 0,
    })

  max_score = max([item['score'] for item in categories] or [0])
  for item in categories:
    item['percent'] = round(item['score'] / max_score * 100) if max_score else 0

  rank_info = build_dashboard_rank(worker_name)
  total_score = round(sum(item['score'] for item in categories), 2)

  return {
    'year': year,
    'categories': categories,
    'total_score': total_score,
    'total_count': sum(item['count'] for item in categories),
    'approved_application_count': sum(item['approved_count'] for item in categories),
    'rank': rank_info['rank'],
    'rank_total': rank_info['rank_total'],
    'period': rank_info['period'],
    'period_score': rank_info['period_score'],
  }


def build_dashboard_rank(worker_name):
  from scores.views import (
    collect_worker_names,
    current_period,
    getJixiaoByItemsLimit,
    getDemocacyScore,
    get_season_str,
    get_worker_profiles,
    updateScoreOfWorkers,
  )

  period_year, period_month = current_period()
  period = get_season_str(period_year, period_month)
  worker_profiles = get_worker_profiles()
  worker_names = collect_worker_names(worker_profiles)
  updateScoreOfWorkers(period_year, period_month, worker_names)
  ranking_scores = getJixiaoByItemsLimit(worker_names, period_year, period_month)
  getDemocacyScore(period, ranking_scores)
  sorted_scores = sorted(ranking_scores.items(), key=lambda item: item[1][2], reverse=True)

  for index, item in enumerate(sorted_scores, start=1):
    if item[0] == worker_name:
      return {
        'rank': index,
        'rank_total': len(sorted_scores),
        'period': period,
        'period_score': round(item[1][2], 2),
      }

  return {
    'rank': None,
    'rank_total': len(sorted_scores),
    'period': period,
    'period_score': 0,
  }



def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, '已注册')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'email已注册')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          
          userProfile = UserProfileInfo(
            user_id=user.id,
            profile_phone='18602038888',
            profile_job_type='其他',
            profile_pic='profile_pics/selfie.png',
            is_approved=False,
          )
          userProfile.save()

          messages.success(request, '注册成功，请等待管理员审批；审批前可以登录查看，不能提交工作量。')
          return redirect('login')
    else:
      messages.error(request, '两次输入的密码不一致')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')



def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, '已登录')
      return redirect('dashboard')
    else:
      messages.error(request, '密码错误')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, '已退出')
    return redirect('login')



def get_or_create_profile(user):
    profile, _ = UserProfileInfo.objects.get_or_create(
      user=user,
      defaults={
        'profile_phone': 0,
        'profile_job_type': '其他',
        'profile_pic': 'profile_pics/selfie.png',
      }
    )
    return profile


def dashboard(request):
    """主页 / 工作台：个人信息 + 工作统计。"""

    if not request.user.is_authenticated:
      return redirect('login')

    my_forms = {"user_form":0,"profile_form":0}
    #if POST  then update info
    if request.method =='POST':
      isUpdate = updateInfo(request,my_forms)
      if isUpdate:
        return redirect('login')
      else:
        return redirect('dashboard')

    #not POST, then show personal info
    else:
      user_basic = request.user
      user_profile = get_or_create_profile(user_basic)
      #给user_form，profile_form赋值，传回前端，就可以在html上显示出来
      #initial={'password':''} 的意思是初始化为空，当用户更新信息时不显示数据库中存的用户密码
      user_form = UserForm(initial={'password':''},instance=user_basic)
      profile_form = UserProfileInfoForm(instance=user_profile)

      #get all types of work info
      myName = worker_display_name(user_basic)
      thisYear = datetime.datetime.now().year
      workSummary = build_dashboard_work_summary(user_basic, myName, thisYear)

      context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "website": user_profile.profile_site,
            "phone_number": user_profile.profile_phone,
            "selfie": user_profile.profile_pic,
            "description": user_profile.profile_descption,
            "can_submit_work": user_profile.can_submit_work,
            "approval_status": "已审批" if user_profile.is_approved else "待审批",
            "workSummary": workSummary,
            }

      return render(request,'accounts/dashboard.html',context)


def work_applications(request):
    """主页 / 工作量申请：提交工作量申请 + 流程历史。"""

    if not request.user.is_authenticated:
      return redirect('login')

    if request.method == 'POST':
      return create_work_application(request)

    user_profile = get_or_create_profile(request.user)
    context = {
      "can_submit_work": user_profile.can_submit_work,
      "approval_status": "已审批" if user_profile.is_approved else "待审批",
      "work_application_form": WorkApplicationForm(),
      "myApplications": WorkApplication.objects.filter(
        applicant=request.user).select_related('reviewer'),
      "ORDER_TYPES": ORDER_TYPES,
      "FAULTY_TYPES": FAULTY_TYPES,
      "MANUFA_TYPES": MANUFA_TYPES,
    }
    return render(request, 'accounts/work_applications.html', context)


def create_work_application(request):
    if not request.user.is_authenticated:
      return redirect('login')

    if request.user.is_superuser:
      messages.error(request, '超级管理员不参与绩效积分，不能提交工作量申请。')
      return redirect('work_applications')

    user_profile = get_or_create_profile(request.user)
    if not user_profile.can_submit_work:
      messages.error(request, '账号尚未审批，暂不能提交工作量申请。')
      return redirect('work_applications')

    form = WorkApplicationForm(request.POST, request.FILES)
    if form.is_valid():
      application = form.save(commit=False)
      application.applicant = request.user
      application.save()
      messages.success(request, '工作量申请已提交，等待审批人审批。')
    else:
      messages.error(request, form.errors)
    return redirect('work_applications')


def approvals(request):
    """审批人待办：展示指定给当前用户、待审批的工作量申请。"""
    if not request.user.is_authenticated:
      return redirect('login')

    pending = WorkApplication.objects.filter(
      reviewer=request.user, status='pending').order_by('created_at')
    reviewed = WorkApplication.objects.filter(
      reviewer=request.user).exclude(status='pending').order_by('-reviewed_at')[:50]

    context = {
      'pending': pending,
      'reviewed': reviewed,
      'pending_count': pending.count(),
    }
    return render(request, 'accounts/approvals.html', context)


def approve_work_application(request, pk):
    application = get_object_or_404(WorkApplication, pk=pk)
    if application.reviewer_id != request.user.id:
      messages.error(request, '你不是该申请的审批人，无法操作。')
      return redirect('approvals')
    if request.method == 'POST':
      application.status = 'approved'
      application.review_comment = request.POST.get('review_comment', '')
      application.reviewed_at = timezone.now()
      application.save()
      sync_application_work_item(application)
      score_year, score_month = refresh_scores_for_application(application)
      messages.success(
        request,
        '已审批通过，%s-%s 的积分已写入总分表。' % (score_year, score_month)
      )
    return redirect('approvals')


def reject_work_application(request, pk):
    application = get_object_or_404(WorkApplication, pk=pk)
    if application.reviewer_id != request.user.id:
      messages.error(request, '你不是该申请的审批人，无法操作。')
      return redirect('approvals')
    if request.method == 'POST':
      was_approved = application.status == 'approved'
      application.status = 'rejected'
      application.review_comment = request.POST.get('review_comment', '')
      application.reviewed_at = timezone.now()
      application.save()
      if was_approved:
        delete_application_work_item(application)
        refresh_scores_for_application(application)
      messages.success(request, '已驳回，申请人可在待办中修改后重新提交。')
    return redirect('approvals')


def edit_work_application(request, pk):
    """申请人修改自己的申请（被驳回或待审批均可），保存后重新进入待审批。"""
    application = get_object_or_404(WorkApplication, pk=pk, applicant=request.user)
    if request.method == 'POST':
      form = WorkApplicationForm(request.POST, request.FILES, instance=application)
      if form.is_valid():
        app = form.save(commit=False)
        app.applicant = request.user
        app.status = 'pending'
        app.review_comment = ''
        app.reviewed_at = None
        app.save()
        messages.success(request, '已重新提交，等待审批人审批。')
        return redirect('work_applications')
      else:
        messages.error(request, form.errors)
    else:
      form = WorkApplicationForm(instance=application)
    return render(request, 'accounts/edit_work_application.html', {
      'form': form,
      'application': application,
    })


def delete_work_application(request, pk):
    application = get_object_or_404(WorkApplication, pk=pk, applicant=request.user)
    if request.method == 'POST':
      application.delete()
      messages.success(request, '申请已删除。')
    return redirect('work_applications')




def updateInfo(request,my_form):

    if request.method == 'POST':
        # 只允许修改当前登录用户自己的资料；表单里的 inputUsername 是
        # readonly 展示用字段，客户端可以伪造，不能作为身份依据。
        user_basic = request.user
        user_pofile = UserProfileInfo.objects.get(user_id=user_basic.id)
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        #print(request.FILES['inputProfilePic'])

        #有instance的时候更新信息，没有instance的时候，新增信息
        user_form = UserForm(data=request.POST,instance=user_basic)
        profile_form = UserProfileInfoForm(data=request.POST,instance=user_pofile)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()
            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            pf = profile_form.save(commit=False)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            pf.user = user
            # Check if they provided a profile picture

           # pf.profile_pic = request.FILES['inputProfilePic']
            if 'inputProfilePic' in request.FILES:
                print('found it!!!!')
                # If yes, then grab it from the POST form reply
                pf.profile_pic = request.FILES['inputProfilePic']

            pf.profile_phone = request.POST.get('inputPhoneNumber')
            pf.profile_site = request.POST.get('inputPersonalWebsite')
            pf.profile_descption= request.POST.get('inputDesciption')

            # Now save model
            pf.save()
            my_form['user_form'] = user_form
            my_form['profile_form'] = profile_form
            return True

        else:
            # One of the forms was invalid if this else gets called.
            messages.error(request, '%s %s' % (user_form.errors, profile_form.errors))
            return False

    return False



# def dashboard(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return redirect('dashboard')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'accounts/dashboard.html', {'form': form})

def printRequest(request):
    print(type(request))   # 打印出request的类型

    print(request.environ)   # 打印出request的header详细信息
    #循环打印出每一个键值对
    for k, v in request.environ.items():
       print(k, v)
