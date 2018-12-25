from django.db import models
from templates.constant_files import WORKERS_NAMES

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
