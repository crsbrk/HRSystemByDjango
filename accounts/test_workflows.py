"""End-to-end functional / use-case tests spanning auth, work-application
lifecycle, scoring and democracy rating."""

import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase

from accounts.models import UserProfileInfo, WorkApplication
from orders.models import Orders
from scores import views as score_views
from scores.models import DemocracyRating, Scores


def make_profile(user, **kwargs):
    defaults = dict(
        profile_phone=0,
        profile_job_type='其他',
        profile_pic='profile_pics/selfie.png',
        is_approved=True,
    )
    defaults.update(kwargs)
    return UserProfileInfo.objects.create(user=user, **defaults)


class AuthGatingTests(TestCase):
    """匿名用户访问受保护页面必须跳转到登录页。"""

    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')

    def test_dashboard_requires_login(self):
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_work_applications_requires_login(self):
        response = self.client.get('/accounts/work-applications/')
        self.assertEqual(response.status_code, 302)

    def test_approvals_requires_login(self):
        response = self.client.get('/accounts/approvals/')
        self.assertEqual(response.status_code, 302)

    def test_democracy_requires_login(self):
        response = self.client.get('/scores/democracy')
        self.assertEqual(response.status_code, 302)


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')

    def _payload(self, **overrides):
        data = {
            'first_name': '三',
            'last_name': '张',
            'username': 'newbie',
            'email': 'newbie@example.com',
            'password': 'StrongPass123',
            'password2': 'StrongPass123',
        }
        data.update(overrides)
        return data

    def test_successful_registration_creates_unapproved_profile(self):
        response = self.client.post('/accounts/register/', self._payload())
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newbie')
        profile = UserProfileInfo.objects.get(user=user)
        self.assertFalse(profile.is_approved)
        self.assertFalse(profile.can_submit_work)

    def test_password_mismatch_is_rejected(self):
        response = self.client.post(
            '/accounts/register/', self._payload(password2='different'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='newbie').exists())

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(username='newbie', password='x')
        response = self.client.post('/accounts/register/', self._payload())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(username='newbie').count(), 1)


class WorkApplicationLifecycleTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.worker = User.objects.create_user(
            username='worker', password='test123456', last_name='测', first_name='试')
        self.profile = make_profile(self.worker)
        self.approver = User.objects.create_user(
            username='manager', password='test123456', last_name='管', first_name='理')
        make_profile(self.approver, role='manager')
        self.score_year, self.score_month = score_views.current_period()
        self.work_date = datetime.date(self.score_year, self.score_month, 15)

    def _create_pending_order_application(self):
        return WorkApplication.objects.create(
            applicant=self.worker,
            reviewer=self.approver,
            work_type='orders',
            title='待审批工单',
            score=2,
            work_num='LIFECYCLE-001',
            work_date=self.work_date,
            workload_allot=1,
            description='全流程测试',
        )

    def test_superuser_cannot_submit_application(self):
        admin = User.objects.create_superuser(
            username='root', password='test123456', email='root@example.com')
        self.client.force_login(admin)
        response = self.client.post('/accounts/work-applications/', {
            'work_type': 'orders',
            'title': '管理员申请',
            'score': '1',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WorkApplication.objects.filter(title='管理员申请').exists())

    def test_non_reviewer_cannot_approve(self):
        application = self._create_pending_order_application()
        stranger = User.objects.create_user(username='stranger', password='x')
        make_profile(stranger)
        self.client.force_login(stranger)
        response = self.client.post(
            '/accounts/work-application/%s/approve/' % application.pk, {})
        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'pending')
        self.assertIsNone(application.materialized_object_id)

    def test_full_approve_then_reject_cycle(self):
        application = self._create_pending_order_application()
        self.client.force_login(self.approver)

        # Approve -> business Order created + score written
        self.client.post(
            '/accounts/work-application/%s/approve/' % application.pk,
            {'review_comment': '同意'})
        application.refresh_from_db()
        self.assertEqual(application.status, 'approved')
        self.assertTrue(Orders.objects.filter(orders_num='LIFECYCLE-001').exists())
        score = Scores.objects.get(
            worker_name='测试',
            score_year_month='%s-%s' % (self.score_year, self.score_month))
        self.assertEqual(score.score_orders, 2)

        # Reject the previously approved item -> business row removed, score reset
        self.client.post(
            '/accounts/work-application/%s/reject/' % application.pk,
            {'review_comment': '撤销'})
        application.refresh_from_db()
        self.assertEqual(application.status, 'rejected')
        self.assertFalse(Orders.objects.filter(orders_num='LIFECYCLE-001').exists())
        self.assertIsNone(application.materialized_object_id)
        score.refresh_from_db()
        self.assertEqual(score.score_orders, 0)

    def test_applicant_can_edit_and_delete_application(self):
        application = self._create_pending_order_application()
        application.status = 'rejected'
        application.save()
        self.client.force_login(self.worker)

        edit = self.client.post(
            '/accounts/work-application/%s/edit/' % application.pk, {
                'work_type': 'orders',
                'title': '修改后的工单',
                'score': '3',
                'work_num': 'LIFECYCLE-001',
                'work_date': self.work_date.isoformat(),
                'reviewer': self.approver.pk,
                'workload_allot': '1',
            })
        self.assertEqual(edit.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.title, '修改后的工单')
        self.assertEqual(application.status, 'pending')

        delete = self.client.post(
            '/accounts/work-application/%s/delete/' % application.pk)
        self.assertEqual(delete.status_code, 302)
        self.assertFalse(WorkApplication.objects.filter(pk=application.pk).exists())


class DemocracyRatingTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.evaluator = User.objects.create_user(
            username='evaluator', password='test123456', last_name='测', first_name='评')
        make_profile(self.evaluator)
        self.target = User.objects.create_user(
            username='target', password='test123456', last_name='被', first_name='评')
        make_profile(self.target)

    def test_submit_creates_ratings_and_blocks_resubmission(self):
        self.client.force_login(self.evaluator)
        season = score_views.get_season_str()

        get_response = self.client.get('/scores/democracy')
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/scores/democracy', {
            'attitude_%s' % self.target.pk: '90',
            'responsibility_%s' % self.target.pk: '80',
            'discipline_%s' % self.target.pk: '70',
        })
        self.assertEqual(post_response.status_code, 302)
        rating = DemocracyRating.objects.get(
            evaluator=self.evaluator, target=self.target, year_season=season)
        self.assertEqual(rating.attitude, 90)
        self.assertEqual(rating.responsibility, 80)
        self.assertEqual(rating.discipline, 70)

        # Already submitted -> redirected to dashboard, no duplicate row
        again = self.client.get('/scores/democracy')
        self.assertEqual(again.status_code, 302)
        self.assertIn('/accounts/dashboard/', again['Location'])
        self.assertEqual(DemocracyRating.objects.filter(
            evaluator=self.evaluator, year_season=season).count(), 1)


class ScoresIndexTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')
        self.worker = User.objects.create_user(
            username='worker', password='test123456', last_name='测', first_name='试')
        make_profile(self.worker)

    def test_scores_index_page_renders_ranking(self):
        response = self.client.get('/scores/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试')
