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
    at_weiguorui = models.IntegerField('韦国锐分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])#IntegerField('加分',choices=FAULTY_SCORE_LIST,default=1)
    at_zhangchen = models.IntegerField('张晨分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_yuqiusi = models.IntegerField('于秋思分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_xuhaipeng = models.IntegerField('许海鹏分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_mamengyang = models.IntegerField('马梦阳分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_suju = models.IntegerField('苏飓分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_guoshaochuan = models.IntegerField('郭少钏分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_huoxiaoge = models.IntegerField('霍晓歌分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_lixiaoxin = models.IntegerField('李晓昕分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_chenjunbiao = models.IntegerField('陈浚标分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_chenlidong = models.IntegerField('陈立栋分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_suweiheng = models.IntegerField('苏伟衡分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_huangmingxian = models.IntegerField('黄铭贤分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_lutianyang = models.IntegerField('陆天洋分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_pengjunlin = models.IntegerField('彭俊霖数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    at_wangzhiwu = models.IntegerField('汪志武分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])

    def __str__(self):
        return self.worker_name


class Responsibility(models.Model):

    #title is project name
    worker_name = models.CharField('员工姓名',editable=False,max_length=200)
    year_season = models.CharField('年季度',editable=False,max_length=200)
    re_weiguorui = models.IntegerField('韦国锐分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_zhangchen = models.IntegerField('张晨分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_yuqiusi = models.IntegerField('于秋思分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_xuhaipeng = models.IntegerField('许海鹏分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_mamengyang = models.IntegerField('马梦阳分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_suju = models.IntegerField('苏飓分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_guoshaochuan = models.IntegerField('郭少钏分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_huoxiaoge = models.IntegerField('霍晓歌分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_lixiaoxin = models.IntegerField('李晓昕分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_chenjunbiao = models.IntegerField('陈浚标分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_chenlidong = models.IntegerField('陈立栋分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_suweiheng = models.IntegerField('苏伟衡分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_huangmingxian = models.IntegerField('黄铭贤分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_lutianyang = models.IntegerField('陆天洋分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_pengjunlin = models.IntegerField('彭俊霖数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    re_wangzhiwu = models.IntegerField('汪志武分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])

    def __str__(self):
        return self.worker_name

class Discipline(models.Model):

    #title is project name
    worker_name = models.CharField('员工姓名',editable=False,max_length=200)
    year_season = models.CharField('年季度',editable=False,max_length=200)
    di_weiguorui = models.IntegerField('韦国锐分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_zhangchen = models.IntegerField('张晨分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_yuqiusi = models.IntegerField('于秋思分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_xuhaipeng = models.IntegerField('许海鹏分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_mamengyang = models.IntegerField('马梦阳分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_suju = models.IntegerField('苏飓分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_guoshaochuan = models.IntegerField('郭少钏分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_huoxiaoge = models.IntegerField('霍晓歌分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_lixiaoxin = models.IntegerField('李晓昕分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_chenjunbiao = models.IntegerField('陈浚标分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_chenlidong = models.IntegerField('陈立栋分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_suweiheng = models.IntegerField('苏伟衡分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_huangmingxian = models.IntegerField('黄铭贤分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_lutianyang = models.IntegerField('陆天洋分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_pengjunlin = models.IntegerField('彭俊霖数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])
    di_wangzhiwu = models.IntegerField('汪志武分数',choices= DEMOCRACY_LIST,default=DEMOCRACY_LIST[0][1])

    def __str__(self):
        return self.worker_name