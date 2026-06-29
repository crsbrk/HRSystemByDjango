from django.db import models
from django.contrib.auth.models import User
from templates.constant_files import DEMOCRACY_LIST


SCORE_CATEGORY_CHOICES = (
    ('posts', '项目类'),
    ('orders', '工单类'),
    ('cutovers', '割接类'),
    ('bonuses', '特殊加分项'),
    ('routine', '日常工作'),
    ('faulty', '故障处理'),
)

SCORE_FORMULA_CHOICES = (
    ('legacy_cap40', '兼容公式：工单/割接/故障/日常封顶40'),
    ('compressed_sum', '分类压缩求和'),
    ('raw_sum', '不压缩直接求和'),
)

SCORE_RULE_ALGORITHM_CHOICES = (
    ('none', '不压缩'),
    ('exponential', '越多加分越少'),
    ('hard_cap', '硬封顶'),
)

class Scores(models.Model):

    #title is project name
    worker_name = models.CharField('员工姓名',max_length=200)
    score_year_month = models.CharField('年月',max_length=200)
    score_posts = models.FloatField('项目分数',default=0.0)
    score_orders = models.FloatField('工单分数',default=0.0)
    score_cutovers = models.FloatField('割接分数',default=0.0)
    score_bonuses = models.FloatField('特殊加分',default=0.0)
    score_faulty = models.FloatField('故障分数',default=0.0)
    score_routine = models.FloatField('日常分数',default=0.0)

    def __str__(self):
        return self.worker_name

    class Meta:
        verbose_name_plural = "总分"
        verbose_name = "总分排名"


class ScoreFormulaPolicy(models.Model):
    """Versioned monthly ranking formula configured by superusers."""

    name = models.CharField('公式名称', max_length=120)
    effective_year = models.PositiveIntegerField('生效年份')
    effective_month = models.PositiveSmallIntegerField('生效月份')
    ranking_formula = models.CharField(
        '排名公式', choices=SCORE_FORMULA_CHOICES, max_length=30, default='legacy_cap40')
    is_active = models.BooleanField('启用', default=True)
    notes = models.TextField('备注', default='', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '绩效公式'
        verbose_name_plural = '绩效公式'
        ordering = ['-effective_year', '-effective_month', '-updated_at']

    def __str__(self):
        return '%s（%s-%s）' % (self.name, self.effective_year, self.effective_month)


class ScoreCategoryRule(models.Model):
    """Per-category compression rule under one formula policy."""

    policy = models.ForeignKey(
        ScoreFormulaPolicy,
        verbose_name='所属公式',
        on_delete=models.CASCADE,
        related_name='category_rules',
    )
    category = models.CharField('工作类别', choices=SCORE_CATEGORY_CHOICES, max_length=20)
    algorithm = models.CharField(
        '算法', choices=SCORE_RULE_ALGORITHM_CHOICES, max_length=20, default='none')
    cap = models.FloatField('上限/逼近值', default=0)
    lambda_value = models.FloatField('压缩系数', default=0)
    weight = models.FloatField('权重', default=1)

    class Meta:
        verbose_name = '分类算法参数'
        verbose_name_plural = '分类算法参数'
        unique_together = ('policy', 'category')
        ordering = ['policy', 'category']

    def __str__(self):
        return '%s - %s' % (self.policy.name, self.get_category_display())


class ScoreRankingSnapshot(models.Model):
    """Durable monthly ranking result with formula snapshot for audit."""

    worker_name = models.CharField('员工姓名', max_length=200)
    score_year = models.PositiveIntegerField('年份')
    score_month = models.PositiveSmallIntegerField('月份')
    raw_posts = models.FloatField('原始项目分数', default=0)
    raw_orders = models.FloatField('原始工单分数', default=0)
    raw_cutovers = models.FloatField('原始割接分数', default=0)
    raw_bonuses = models.FloatField('原始特殊加分', default=0)
    raw_faulty = models.FloatField('原始故障分数', default=0)
    raw_routine = models.FloatField('原始日常分数', default=0)
    final_posts = models.FloatField('公式后项目分数', default=0)
    final_orders = models.FloatField('公式后工单分数', default=0)
    final_cutovers = models.FloatField('公式后割接分数', default=0)
    final_bonuses = models.FloatField('公式后特殊加分', default=0)
    final_faulty = models.FloatField('公式后故障分数', default=0)
    final_routine = models.FloatField('公式后日常分数', default=0)
    work_score = models.FloatField('工作绩效分', default=0)
    democracy_score = models.FloatField('民主测评分', default=0)
    total_score = models.FloatField('总分', default=0)
    rank = models.PositiveIntegerField('排名', default=0)
    policy = models.ForeignKey(
        ScoreFormulaPolicy,
        verbose_name='使用公式',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ranking_snapshots',
    )
    policy_snapshot = models.JSONField('公式快照', default=dict, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '月度排名快照'
        verbose_name_plural = '月度排名快照'
        unique_together = ('worker_name', 'score_year', 'score_month')
        ordering = ['score_year', 'score_month', 'rank', 'worker_name']

    def __str__(self):
        return '%s %s-%s #%s' % (
            self.worker_name, self.score_year, self.score_month, self.rank)



class DemocracyRating(models.Model):
    """民主测评：一条记录 = 某测评人对某被测评人在一个季度的三项打分。

    不再为每个员工写死字段，测评人与被测评人都关联到注册用户，
    支持任意新注册员工自动参与。
    """
    evaluator = models.ForeignKey(
        User, verbose_name='测评人', on_delete=models.CASCADE, related_name='democracy_given')
    target = models.ForeignKey(
        User, verbose_name='被测评人', on_delete=models.CASCADE, related_name='democracy_received')
    year_season = models.CharField('年季度', max_length=200)
    attitude = models.IntegerField('工作态度', choices=DEMOCRACY_LIST, default=DEMOCRACY_LIST[0][1])
    responsibility = models.IntegerField('责任心', choices=DEMOCRACY_LIST, default=DEMOCRACY_LIST[0][1])
    discipline = models.IntegerField('工作纪律', choices=DEMOCRACY_LIST, default=DEMOCRACY_LIST[0][1])

    class Meta:
        verbose_name = '民主测评'
        verbose_name_plural = '民主测评'
        unique_together = ('evaluator', 'target', 'year_season')

    def __str__(self):
        return '%s -> %s (%s)' % (self.evaluator, self.target, self.year_season)
