from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from templates.constant_files import WORKERS_NAMES ,FAULTY_TYPES,FAULTY_SCORE_LIST,MANUFA_TYPES
# Create your models here.


class Faulty(models.Model):

    #title is bonus name
    title = models.CharField('故障名称', max_length=200)
    pj_score = models.IntegerField('加分',choices=FAULTY_SCORE_LIST,default=1)
    pj_type = models.CharField(
        '故障类型', choices=FAULTY_TYPES, max_length=200, default='硬件')
    pj_manufacturer = models.CharField(
        '厂家', choices=MANUFA_TYPES, max_length=200, default='华为')
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

    is_not_delayed = models.BooleanField('处理完成', default=True)
    created_at = models.DateTimeField('开始日期', default=datetime.now, blank=True)
    body = models.TextField('备注', default='', blank=True)  # body is comment

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "故障处理"
        verbose_name = '故障处理'
