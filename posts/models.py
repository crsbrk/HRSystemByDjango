from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from templates.constant_files import WORKERS_NAMES, ORDER_TYPES

# Create your models here.


class Posts(models.Model):

    #title is project name
    title = models.CharField('项目名称', max_length=200)

    pj_score = models.IntegerField('项目加分', default=0)
    pj_leader = models.CharField(
        '完成人员1', choices=WORKERS_NAMES, max_length=200)
    workload_allot = models.FloatField(
        '比例1', validators=[MinValueValidator(0.0), MaxValueValidator(1)], default=0)
    pj_participant1 = models.CharField(
        '完成人员2', choices=WORKERS_NAMES, max_length=200, blank=True)
    workload_allot1 = models.FloatField(
        '比例2', validators=[MinValueValidator(0.0), MaxValueValidator(1)], default=0)
    pj_participant2 = models.CharField(
        '完成人员3', choices=WORKERS_NAMES, max_length=200, blank=True)
    workload_allot2 = models.FloatField(
        '比例3', validators=[MinValueValidator(0.0), MaxValueValidator(1)], default=0)
    pj_participant3 = models.CharField(
        '完成人员4', choices=WORKERS_NAMES, max_length=200, blank=True)
    workload_allot3 = models.FloatField(
        '比例4', validators=[MinValueValidator(0.0), MaxValueValidator(1)], default=0)

    deadline_at = models.DateTimeField(
        '计划完成日期', default=datetime.now, blank=True)
    pj_progress = models.FloatField(
        '当前进度', validators=[MinValueValidator(0.0), MaxValueValidator(1)], default=0)
    is_not_delayed = models.BooleanField('未超时', default=True)
    created_at = models.DateTimeField('开始日期', default=datetime.now, blank=True)
    body = models.TextField('备注', default='', blank=True)  # body is comment

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "项目"
        verbose_name = "项目加分"
