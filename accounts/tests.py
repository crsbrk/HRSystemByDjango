import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from accounts.models import UserProfileInfo, WorkApplication
from accounts.views import build_dashboard_rank
from orders.models import Orders
from posts.models import Posts
from scores import views as score_views
from scores.models import ScoreFormulaPolicy, Scores


class WorkApplicationTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.user = User.objects.create_user(
            username='worker',
            password='test123456',
            last_name='测',
            first_name='试',
        )
        self.profile = UserProfileInfo.objects.create(
            user=self.user,
            profile_phone=0,
            profile_job_type='其他',
            profile_pic='profile_pics/selfie.png',
            is_approved=False,
        )
        # 审批人：管理员角色、非超级管理员
        self.approver = User.objects.create_user(
            username='manager',
            password='test123456',
            last_name='管',
            first_name='理',
        )
        UserProfileInfo.objects.create(
            user=self.approver,
            profile_phone=0,
            profile_job_type='其他',
            profile_pic='profile_pics/selfie.png',
            role='manager',
            is_approved=True,
        )

    def test_unapproved_user_cannot_submit_work_application(self):
        self.client.force_login(self.user)
        response = self.client.post('/accounts/work-applications/', {
            'form_type': 'work_application',
            'work_type': 'orders',
            'title': '未审批申请',
            'score': '1',
            'description': '测试',
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(WorkApplication.objects.exists())

    def test_approved_user_can_submit_work_application(self):
        self.profile.is_approved = True
        self.profile.save()
        self.client.force_login(self.user)

        response = self.client.post('/accounts/work-applications/', {
            'form_type': 'work_application',
            'work_type': 'orders',
            'title': '已审批申请',
            'score': '1',
            'description': '测试',
            'reviewer': self.approver.pk,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(WorkApplication.objects.filter(title='已审批申请').exists())

    def test_duplicate_application_submission_is_allowed_but_marked_suspected(self):
        self.profile.is_approved = True
        self.profile.save()
        score_year, score_month = score_views.current_period()
        work_date = datetime.date(score_year, score_month, 15)
        Orders.objects.create(
            orders_num='DUP-ORDER-001',
            title='重复工单',
            pj_score=1,
            pj_leader='测试',
            workload_allot=1,
            deadline_at=work_date,
            created_at=timezone.now(),
            is_not_delayed=True,
            is_finished=True,
            body='已有记录',
        )
        self.client.force_login(self.user)

        response = self.client.post('/accounts/work-applications/', {
            'form_type': 'work_application',
            'work_type': 'orders',
            'title': '重复工单',
            'score': '1',
            'work_num': 'DUP-ORDER-001',
            'work_date': work_date.isoformat(),
            'description': '允许提交但提醒审批人',
            'reviewer': self.approver.pk,
        })

        self.assertEqual(response.status_code, 302)
        application = WorkApplication.objects.get(title='重复工单')
        self.assertEqual(application.status, 'pending')
        self.assertEqual(application.duplicate_status, 'suspected')
        self.assertTrue(application.duplicate_signature)

    def test_suspected_duplicate_cannot_be_approved_without_override_reason(self):
        self.profile.is_approved = True
        self.profile.save()
        score_year, score_month = score_views.current_period()
        application = WorkApplication.objects.create(
            applicant=self.user,
            reviewer=self.approver,
            work_type='orders',
            title='疑似重复工单',
            score=1,
            work_num='DUP-APPROVE-001',
            work_date=datetime.date(score_year, score_month, 15),
            description='审批时需要确认',
            duplicate_status='suspected',
            duplicate_signature='orders|DUP-APPROVE-001',
        )
        self.client.force_login(self.approver)

        response = self.client.post(
            '/accounts/work-application/%s/approve/' % application.pk,
            {'review_comment': 'ok'},
        )

        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'pending')
        self.assertIsNone(application.materialized_object_id)

    def test_duplicate_override_allows_approval_and_stores_audit(self):
        self.profile.is_approved = True
        self.profile.save()
        score_year, score_month = score_views.current_period()
        application = WorkApplication.objects.create(
            applicant=self.user,
            reviewer=self.approver,
            work_type='orders',
            title='确认非重复工单',
            score=1,
            work_num='DUP-OVERRIDE-001',
            work_date=datetime.date(score_year, score_month, 15),
            description='审批确认通过',
            duplicate_status='suspected',
            duplicate_signature='orders|DUP-OVERRIDE-001',
        )
        self.client.force_login(self.approver)

        response = self.client.post(
            '/accounts/work-application/%s/approve/' % application.pk,
            {
                'review_comment': 'ok',
                'duplicate_confirmed': 'on',
                'duplicate_override_reason': '同名编号来自不同批次，确认不是重复。',
            },
        )

        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'approved')
        self.assertEqual(application.duplicate_status, 'overridden')
        self.assertEqual(application.duplicate_override_by, self.approver)
        self.assertEqual(application.duplicate_override_reason, '同名编号来自不同批次，确认不是重复。')
        self.assertTrue(Orders.objects.filter(orders_num='DUP-OVERRIDE-001').exists())

    def test_dashboard_shows_work_summary_instead_of_order_table(self):
        self.profile.is_approved = True
        self.profile.save()
        now = timezone.now()
        Orders.objects.create(
            orders_num='GD-001',
            title='网络工单',
            pj_score=1,
            pj_leader='测试',
            workload_allot=1,
            deadline_at=now,
            created_at=now,
            is_not_delayed=True,
            is_finished=True,
            body='完成',
        )
        self.client.force_login(self.user)

        response = self.client.get('/accounts/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '工作统计')
        self.assertContains(response, '工单类')
        self.assertContains(response, '割接类')
        self.assertContains(response, '项目类')
        self.assertContains(response, '日常工作')
        self.assertContains(response, '故障处理')
        self.assertContains(response, '特殊加分项')
        self.assertContains(response, '绩效排名')
        self.assertNotContains(response, '<th scope="col">工单号</th>')
        self.assertNotContains(response, '<th scope="col">工单名</th>')
        # 工作量申请已拆分到独立页面，工作台不再包含提交表单
        self.assertNotContains(response, '提交工作量申请')

    def test_dashboard_rank_uses_active_formula_snapshot(self):
        self.profile.is_approved = True
        self.profile.save()
        other_user = User.objects.create_user(
            username='other',
            password='test123456',
            last_name='对',
            first_name='照',
        )
        UserProfileInfo.objects.create(
            user=other_user,
            profile_phone=0,
            profile_job_type='其他',
            profile_pic='profile_pics/selfie.png',
            is_approved=True,
        )
        score_year, score_month = score_views.current_period()
        work_date = datetime.datetime(score_year, score_month, 15)
        ScoreFormulaPolicy.objects.create(
            name='不压缩公式',
            effective_year=score_year,
            effective_month=score_month,
            ranking_formula='raw_sum',
            is_active=True,
        )
        Orders.objects.create(
            orders_num='RAW-RANK-001',
            title='大量工单',
            pj_score=100,
            pj_leader='测试',
            workload_allot=1,
            deadline_at=work_date,
            created_at=work_date,
            is_not_delayed=True,
            is_finished=True,
            body='完成',
        )
        Posts.objects.create(
            title='对照项目',
            pj_score=50,
            pj_leader='对照',
            workload_allot=1,
            deadline_at=work_date,
            created_at=work_date,
            pj_progress=1,
            is_not_delayed=True,
            body='完成',
        )

        rank_info = build_dashboard_rank('测试')

        self.assertEqual(rank_info['rank'], 1)
        self.assertEqual(rank_info['period_score'], 100)

    def test_work_applications_page_shows_form_and_history(self):
        self.profile.is_approved = True
        self.profile.save()
        self.client.force_login(self.user)

        response = self.client.get('/accounts/work-applications/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '提交工作量申请')
        self.assertContains(response, '流程历史')

    def test_approving_work_application_writes_score_record(self):
        self.profile.is_approved = True
        self.profile.save()
        score_year, score_month = score_views.current_period()
        application = WorkApplication.objects.create(
            applicant=self.user,
            reviewer=self.approver,
            work_type='faulty',
            title='已处理故障',
            score=2,
            work_date=datetime.date(score_year, score_month, 15),
            description='测试审批后写入分数',
        )
        self.client.force_login(self.approver)

        response = self.client.post(
            '/accounts/work-application/%s/approve/' % application.pk,
            {'review_comment': 'ok'},
        )

        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'approved')
        score = Scores.objects.get(
            worker_name='测试',
            score_year_month='%s-%s' % (score_year, score_month),
        )
        self.assertEqual(score.score_faulty, 2)

    def test_approving_application_creates_work_item_with_participant_ratios(self):
        self.profile.is_approved = True
        self.profile.save()
        score_year, score_month = score_views.current_period()
        application = WorkApplication.objects.create(
            applicant=self.user,
            reviewer=self.approver,
            work_type='orders',
            title='多人协作工单',
            score=2,
            work_num='APP-ORDER-001',
            work_subtype='DNS',
            work_date=datetime.date(score_year, score_month, 15),
            workload_allot=0.6,
            pj_participant1='管理',
            workload_allot1=0.4,
            description='测试生成业务工单',
        )
        self.client.force_login(self.approver)

        response = self.client.post(
            '/accounts/work-application/%s/approve/' % application.pk,
            {'review_comment': 'ok'},
        )

        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        order = Orders.objects.get(pk=application.materialized_object_id)
        self.assertEqual(order.orders_num, 'APP-ORDER-001')
        self.assertEqual(order.pj_leader, '测试')
        self.assertEqual(order.pj_participant1, '管理')
        self.assertEqual(order.workload_allot, 0.6)
        self.assertEqual(order.workload_allot1, 0.4)

        applicant_score = Scores.objects.get(
            worker_name='测试',
            score_year_month='%s-%s' % (score_year, score_month),
        )
        participant_score = Scores.objects.get(
            worker_name='管理',
            score_year_month='%s-%s' % (score_year, score_month),
        )
        self.assertAlmostEqual(applicant_score.score_orders, 1.2)
        self.assertAlmostEqual(participant_score.score_orders, 0.8)
