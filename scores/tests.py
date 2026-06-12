import datetime

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, TestCase

from accounts.models import SiteSetting, UserProfileInfo
from orders.models import Orders
from scores import views as score_views


class ScoresPageTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')

    def test_registered_worker_appears_in_ranking(self):
        user = User.objects.create_user(
            username='new_worker',
            password='test123456',
            first_name='员工',
            last_name='新',
            email='new_worker@example.com',
        )
        UserProfileInfo.objects.create(
            user=user,
            profile_phone=0,
            profile_job_type='其他',
            profile_pic='profile_pics/selfie.png',
            is_approved=True,
        )
        score_year, score_month = score_views.current_period()
        work_date = datetime.datetime(score_year, score_month, 15)
        Orders.objects.create(
            orders_num='T-001',
            title='测试工单',
            pj_score=1,
            pj_leader='新员工',
            workload_allot=1,
            deadline_at=work_date,
            created_at=work_date,
            is_not_delayed=True,
            is_finished=True,
            body='测试备注',
        )

        response = self.client.get('/scores/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '新员工')
        self.assertContains(response, 'score-avatar')
        self.assertContains(response, '已审批')

    def test_site_setting_renders_in_layout(self):
        setting = SiteSetting.load()
        setting.project_name = '内部积分平台'
        setting.footer_text = '测试运维团队'
        setting.save()

        response = self.client.get('/accounts/login/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '内部积分平台')
        self.assertContains(response, '测试运维团队')

    def test_seed_test_data_command_creates_work_items(self):
        call_command('seed_test_data', count=1, verbosity=0)

        self.assertTrue(User.objects.filter(username='tester1').exists())
        self.assertTrue(Orders.objects.filter(title='测试工单 01').exists())
