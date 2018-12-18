from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Bonuses(models.Model):
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
    #title is bonus name
    title = models.CharField('加分项目名称',max_length=200)
    pj_score = models.IntegerField('项目加分',default=0)
    pj_leader = models.CharField('完成人员1',choices=WORKERS_NAMES,max_length=200)
    workload_allot = models.FloatField('比例1', validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)
    pj_participant1 = models.CharField('完成人员2',choices=WORKERS_NAMES,max_length=200, blank=True)
    workload_allot1 = models.FloatField('比例2',validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)
    pj_participant2 = models.CharField('完成人员3',choices=WORKERS_NAMES,max_length=200, blank=True)
    workload_allot2= models.FloatField('比例3',validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)
    pj_participant3 = models.CharField('完成人员4',choices=WORKERS_NAMES,max_length=200,blank=True)
    workload_allot3 = models.FloatField('比例4',validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)


    is_delayed = models.BooleanField('未在别处加分',default=True)
    created_at = models.DateTimeField('开始日期',default=datetime.now, blank=True)
    body = models.TextField('备注', default='', blank=True)#body is comment

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "特殊加分"
        verbose_name = '特殊加分'
