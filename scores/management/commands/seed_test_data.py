import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserProfileInfo
from bonuses.models import Bonuses
from cutovers.models import Cutovers
from faulty.models import Faulty
from orders.models import Orders
from posts.models import Posts
from routine.models import Routine
from scores.models import DemocracyRating
from scores.views import current_period, get_season_str
from templates.constant_files import DEMOCRACY_LIST


DEMO_USERS = (
    ('tester1', '测试', '员工1'),
    ('tester2', '测试', '员工2'),
    ('tester3', '测试', '员工3'),
    ('tester4', '测试', '员工4'),
)


class Command(BaseCommand):
    help = '随机生成工单、割接、项目、日常工作、故障处理、特殊加分测试数据。'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=8, help='每类工作生成数量，默认 8。')
        parser.add_argument('--password', default='test123456', help='演示用户默认密码。')

    def handle(self, *args, **options):
        count = options['count']
        workers = self.ensure_demo_workers(options['password'])
        # scores 排名计算的是“上个月”的数据，测试数据需落在该月才会出现在排名里。
        score_year, score_month = current_period()
        today = timezone.now().replace(year=score_year, month=score_month, day=15)

        for index in range(count):
            leader = random.choice(workers)
            participant = random.choice([name for name in workers if name != leader] or workers)
            split = random.choice([0.6, 0.7, 0.8, 1.0])
            second_split = round(1 - split, 2) if participant != leader else 0

            Orders.objects.create(
                orders_num='TEST-ORDER-%04d' % index,
                title='测试工单 %02d' % (index + 1),
                pj_score=1,
                pj_leader=leader,
                workload_allot=split,
                pj_participant1=participant if second_split else '',
                workload_allot1=second_split,
                orders_type=random.choice(['物联网', 'DNS', 'AMF', 'SMF', '其他']),
                deadline_at=today,
                is_not_delayed=True,
                is_finished=True,
                created_at=today,
                body='随机测试数据',
            )
            Cutovers.objects.create(
                cutover_num='TEST-CUT-%04d' % index,
                title='测试割接 %02d' % (index + 1),
                pj_leader=leader,
                deadline_at=today,
                is_not_delayed=True,
                body='随机测试数据',
            )
            Posts.objects.create(
                title='测试项目 %02d' % (index + 1),
                pj_score=random.choice([10, 15, 20, 25]),
                pj_leader=leader,
                workload_allot=split,
                pj_participant1=participant if second_split else '',
                workload_allot1=second_split,
                deadline_at=today,
                pj_progress=1,
                is_not_delayed=True,
                created_at=today,
                body='随机测试数据',
            )
            Routine.objects.create(
                title='测试日常工作 %02d' % (index + 1),
                pj_score=random.choice([1, 2, 3]),
                pj_leader=leader,
                workload_allot=split,
                pj_participant1=participant if second_split else '',
                workload_allot1=second_split,
                is_not_delayed=True,
                created_at=today,
                body='随机测试数据',
            )
            Faulty.objects.create(
                title='测试故障处理 %02d' % (index + 1),
                pj_score=random.choice([1, 2]),
                pj_type=random.choice(['硬件', '软件', '其他']),
                pj_manufacturer=random.choice(['华为', '中兴', '诺基亚', '其他']),
                pj_leader=leader,
                workload_allot=split,
                pj_participant1=participant if second_split else '',
                workload_allot1=second_split,
                is_not_delayed=True,
                created_at=today,
                body='随机测试数据',
            )
            Bonuses.objects.create(
                title='测试特殊加分 %02d' % (index + 1),
                pj_score=random.choice([3, 5, 8, 10]),
                pj_leader=leader,
                workload_allot=split,
                pj_participant1=participant if second_split else '',
                workload_allot1=second_split,
                is_not_delayed=True,
                created_at=today,
                body='随机测试数据',
            )

        democracy_count = self.seed_democracy()

        self.stdout.write(self.style.SUCCESS(
            '已生成测试数据：6 类业务 x %s 条，民主测评 %s 条（季度：%s）。'
            % (count, democracy_count, get_season_str())
        ))

    def seed_democracy(self):
        """让每个注册员工对其他员工生成本季度民主测评打分。"""
        score_values = [value for value, _ in DEMOCRACY_LIST if value]
        users = list(User.objects.filter(is_superuser=False).order_by('id'))
        season_str = get_season_str()
        created = 0
        for evaluator in users:
            for target in users:
                if evaluator.pk == target.pk:
                    continue
                DemocracyRating.objects.update_or_create(
                    evaluator=evaluator,
                    target=target,
                    year_season=season_str,
                    defaults={
                        'attitude': random.choice(score_values),
                        'responsibility': random.choice(score_values),
                        'discipline': random.choice(score_values),
                    },
                )
                created += 1
        return created

    def ensure_demo_workers(self, password):
        workers = []
        for username, last_name, first_name in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'last_name': last_name,
                    'first_name': first_name,
                    'email': '%s@example.com' % username,
                },
            )
            if created:
                user.set_password(password)
                user.save()

            profile, _ = UserProfileInfo.objects.get_or_create(
                user=user,
                defaults={
                    'profile_phone': 0,
                    'profile_job_type': '其他',
                    'profile_pic': 'profile_pics/selfie.png',
                    'is_approved': True,
                },
            )
            if not profile.is_approved:
                profile.is_approved = True
                profile.save()

            workers.append('%s%s' % (user.last_name, user.first_name))
        return workers
