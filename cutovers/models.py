from django.db import models
from datetime import datetime
from templates.constant_files import WORKERS_NAMES

# Create your models here.
class Cutovers(models.Model):

    #title is project name
    cutover_num =  models.CharField('割接工单编号',max_length=200)
    title = models.CharField('割接名称',max_length=200)
    pj_leader = models.CharField('割接负责人',choices=WORKERS_NAMES,max_length=200)


    deadline_at = models.DateTimeField('割接日期',default=datetime.now)
    is_not_delayed = models.BooleanField('完成',default=False)

    body = models.TextField('备注', default='', blank=True)#body is comment

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "割接"
        verbose_name = '割接'
