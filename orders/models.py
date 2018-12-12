from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Orders(models.Model):
    #title is project name

    ORDER_TYPES = (
        ('行业', '行业'),
        ('物联网', '物联网'),
        ('内容计费', '内容计费'),
        ('DNS', 'DNS'),
        ('PCRF', 'PCRF'),
        ('国际漫游', '国际漫游'),
        ('SGSN/MME局数据', 'SGSN/MME局数据'),
        ('SGW/PGW局数据', 'SGW/PGW局数据'),
        ('其他', '其他'),
    )
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
    orders_num = models.CharField('工单编号',max_length=200)
    title = models.CharField('工单名称',max_length=200)
    pj_score = models.IntegerField('工单加分',default=0)
    pj_leader = models.CharField('完成人员1',choices=WORKERS_NAMES,max_length=200)
    workload_allot = models.FloatField('比例1',validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)
    pj_participant1 = models.CharField('完成人员2',max_length=200,choices=WORKERS_NAMES, blank=True)
    workload_allot1 = models.FloatField('比例2',validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)
    pj_participant2 = models.CharField('完成人员3',max_length=200, choices=WORKERS_NAMES,blank=True)
    workload_allot2= models.FloatField('比例3',validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)
    pj_participant3 = models.CharField('完成人员4',max_length=200,choices=WORKERS_NAMES,blank=True)
    workload_allot3 = models.FloatField('比例4',validators=[MinValueValidator(0.0), MaxValueValidator(1)],default=0)
    orders_type = models.CharField('工单类型:',max_length=24,choices=ORDER_TYPES,default='物联网')
    deadline_at = models.DateTimeField('工单完成日期',default=datetime.now, blank=True)
    is_delayed = models.BooleanField('超时',default=False)
    is_finished = models.BooleanField('完成',default=False)
    created_at = models.DateTimeField('登记日期',default=datetime.now, blank=True)
    body = models.TextField('备注', default='', blank=True)#body is comment

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "工单"
        verbose_name = '工单'
