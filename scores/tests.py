import datetime
import math

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, TestCase

from accounts.models import SiteSetting, UserProfileInfo
from orders.models import Orders
from scores.models import (
    ScoreCategoryRule,
    ScoreFormulaPolicy,
    ScoreRankingSnapshot,
)
from scores.services.formulas import (
    calculate_category_score,
    calculate_work_score,
    generate_ranking_snapshots,
    get_policy_for_period,
)
from scores import views as score_views
from scores.models import Scores


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
        self.assertTrue(ScoreRankingSnapshot.objects.filter(worker_name='新员工').exists())
        self.assertContains(response, '当前兼容公式')

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


class ScoreFormulaPolicyTests(TestCase):
    def test_policy_selection_uses_latest_active_policy_before_period(self):
        old_policy = ScoreFormulaPolicy.objects.create(
            name='旧公式',
            effective_year=2026,
            effective_month=1,
            ranking_formula='legacy_cap40',
            is_active=True,
        )
        new_policy = ScoreFormulaPolicy.objects.create(
            name='七月新公式',
            effective_year=2026,
            effective_month=7,
            ranking_formula='raw_sum',
            is_active=True,
        )

        self.assertEqual(get_policy_for_period(2026, 6), old_policy)
        self.assertEqual(get_policy_for_period(2026, 7), new_policy)
        self.assertEqual(get_policy_for_period(2026, 12), new_policy)

    def test_legacy_formula_matches_current_cap40_behavior(self):
        policy = ScoreFormulaPolicy.objects.create(
            name='兼容公式',
            effective_year=2000,
            effective_month=1,
            ranking_formula='legacy_cap40',
            is_active=True,
        )
        raw_scores = {
            'posts': 5,
            'orders': 50,
            'cutovers': 3,
            'bonuses': 2,
            'faulty': 1,
            'routine': 1,
        }

        result = calculate_work_score(raw_scores, policy)

        self.assertEqual(result['work_score'], 47)
        self.assertEqual(result['final_posts'], 5)
        self.assertEqual(result['final_orders'], 50)
        self.assertEqual(result['final_cutovers'], 3)

    def test_compressed_sum_applies_category_rules(self):
        policy = ScoreFormulaPolicy.objects.create(
            name='压缩公式',
            effective_year=2026,
            effective_month=7,
            ranking_formula='compressed_sum',
            is_active=True,
        )
        orders_rule = ScoreCategoryRule.objects.create(
            policy=policy,
            category='orders',
            algorithm='exponential',
            cap=10,
            lambda_value=0.5,
            weight=1,
        )
        ScoreCategoryRule.objects.create(
            policy=policy,
            category='posts',
            algorithm='none',
            weight=1,
        )

        self.assertAlmostEqual(
            calculate_category_score(2, orders_rule),
            10 * (1 - math.exp(-1)),
        )
        result = calculate_work_score({
            'posts': 3,
            'orders': 2,
            'cutovers': 0,
            'bonuses': 0,
            'faulty': 0,
            'routine': 0,
        }, policy)

        self.assertAlmostEqual(result['final_posts'], 3)
        self.assertAlmostEqual(result['final_orders'], 10 * (1 - math.exp(-1)))
        self.assertAlmostEqual(result['work_score'], 3 + 10 * (1 - math.exp(-1)))

    def test_snapshot_generation_stores_policy_snapshot_and_rank(self):
        policy = ScoreFormulaPolicy.objects.create(
            name='快照公式',
            effective_year=2026,
            effective_month=7,
            ranking_formula='raw_sum',
            is_active=True,
        )
        Scores.objects.create(
            worker_name='张三',
            score_year_month='2026-7',
            score_posts=1,
            score_orders=2,
            score_cutovers=3,
            score_bonuses=4,
            score_faulty=5,
            score_routine=6,
        )

        snapshots = generate_ranking_snapshots(2026, 7, ['张三'])

        self.assertEqual(len(snapshots), 1)
        snapshot = ScoreRankingSnapshot.objects.get(worker_name='张三')
        self.assertEqual(snapshot.policy, policy)
        self.assertEqual(snapshot.raw_orders, 2)
        self.assertEqual(snapshot.work_score, 21)
        self.assertEqual(snapshot.total_score, 21)
        self.assertEqual(snapshot.rank, 1)
        self.assertEqual(snapshot.policy_snapshot['ranking_formula'], 'raw_sum')
