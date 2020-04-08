from django.db import models
from templates.constant_files import WORKERS_NAMES,DEMOCRACY_LIST



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

class Attitude(models.Model):

    #title is project name
    worker_name = models.CharField('员工姓名', editable=False, max_length=200)
    year_season = models.CharField('年季度', editable=False, max_length=200)
    at_weiguorui = models.IntegerField('韦国锐分数',choices= DEMOCRACY_LIST)#IntegerField('加分',choices=FAULTY_SCORE_LIST,default=1)
    at_zhangchen = models.FloatField('张晨分数',default=0.0)
    at_yuqiusi = models.FloatField('于秋思分数',default=0.0)
    at_liufeng = models.FloatField('刘峰分数',default=0.0)
    at_changxiaobo = models.FloatField('常晓波分数',default=0.0)
    at_suju = models.FloatField('苏飓分数',default=0.0)
    at_guoshaochuan = models.FloatField('郭少钏分数',default=0.0)
    at_huoxiaoge = models.FloatField('霍晓歌分数',default=0.0)
    at_lixiaoxin = models.FloatField('李晓昕分数',default=0.0)
    at_liujiang = models.FloatField('刘江分数',default=0.0)
    at_chenlidong = models.FloatField('陈立栋分数',default=0.0)
    at_suweiheng = models.FloatField('苏伟衡分数',default=0.0)
    at_yangxiao = models.FloatField('杨晓分数',default=0.0)
    at_liulei = models.FloatField('刘雷分数',default=0.0)
    at_huangqiangxu = models.FloatField('黄锵栩分数',default=0.0)
    at_wangzhiwu = models.FloatField('汪志武分数',default=0.0)

    def __str__(self):
        return self.worker_name


class Responsibility(models.Model):

    #title is project name
    worker_name = models.CharField('员工姓名',editable=False,max_length=200)
    year_season = models.CharField('年季度',editable=False,max_length=200)
    re_weiguorui = models.FloatField('韦国锐分数',default=0.0)
    re_zhangchen = models.FloatField('张晨分数',default=0.0)
    re_yuqiusi = models.FloatField('于秋思分数',default=0.0)
    re_liufeng = models.FloatField('刘峰分数',default=0.0)
    re_changxiaobo = models.FloatField('常晓波分数',default=0.0)
    re_suju = models.FloatField('苏飓分数',default=0.0)
    re_guoshaochuan = models.FloatField('郭少钏分数',default=0.0)
    re_huoxiaoge = models.FloatField('霍晓歌分数',default=0.0)
    re_lixiaoxin = models.FloatField('李晓昕分数',default=0.0)
    re_liujiang = models.FloatField('刘江分数',default=0.0)
    re_chenlidong = models.FloatField('陈立栋分数',default=0.0)
    re_suweiheng = models.FloatField('苏伟衡分数',default=0.0)
    re_yangxiao = models.FloatField('杨晓分数',default=0.0)
    re_liulei = models.FloatField('刘雷分数',default=0.0)
    re_huangqiangxu = models.FloatField('黄锵栩分数',default=0.0)
    re_wangzhiwu = models.FloatField('汪志武分数',default=0.0)

    def __str__(self):
        return self.worker_name

class Discipline(models.Model):

    #title is project name
    worker_name = models.CharField('员工姓名',editable=False,max_length=200)
    year_season = models.CharField('年季度',editable=False,max_length=200)
    di_weiguorui = models.FloatField('韦国锐分数',default=0.0)
    di_zhangchen = models.FloatField('张晨分数',default=0.0)
    di_yuqiusi = models.FloatField('于秋思分数',default=0.0)
    di_liufeng = models.FloatField('刘峰分数',default=0.0)
    di_changxiaobo = models.FloatField('常晓波分数',default=0.0)
    di_suju = models.FloatField('苏飓分数',default=0.0)
    di_guoshaochuan = models.FloatField('郭少钏分数',default=0.0)
    di_huoxiaoge = models.FloatField('霍晓歌分数',default=0.0)
    di_lixiaoxin = models.FloatField('李晓昕分数',default=0.0)
    di_liujiang = models.FloatField('刘江分数',default=0.0)
    di_chenlidong = models.FloatField('陈立栋分数',default=0.0)
    di_suweiheng = models.FloatField('苏伟衡分数',default=0.0)
    di_yangxiao = models.FloatField('杨晓分数',default=0.0)
    di_liulei = models.FloatField('刘雷分数',default=0.0)
    di_huangqiangxu = models.FloatField('黄锵栩分数',default=0.0)
    di_wangzhiwu = models.FloatField('汪志武分数',default=0.0)

    def __str__(self):
        return self.worker_name