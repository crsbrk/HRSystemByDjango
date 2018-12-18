from django.db import models
from datetime import datetime


# Create your models here.
class Cutovers(models.Model):
    WORKERS_NAMES = (
        ('陈立栋', '陈立栋'),
        ('常晓波', '常晓波'),
        ('刘江', '刘江'),
		('刘雷', '刘雷'),
		('刘峰', '刘峰'),
		('冯庆', '冯庆'),
		('郭少钏', '郭少钏'),
		('于秋思', '于秋思'),
		('苏飓', '苏飓'),
        ('苏伟衡', '苏伟衡'),
        ('杨晓', '杨晓'),
		('霍晓歌', '霍晓歌'),
		('李晓昕', '李晓昕'),
		('韦国锐', '韦国锐'),
		('张晨', '张晨'),
	)
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
