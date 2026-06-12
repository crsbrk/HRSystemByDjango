from django.db import models
from django.contrib.auth.models import User
from templates.constant_files import DEMOCRACY_LIST

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