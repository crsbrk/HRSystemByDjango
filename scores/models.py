from django.db import models

class Scores(models.Model):
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
    worker_name = models.CharField('员工姓名',max_length=200)
    score_year_month = models.CharField('年月',max_length=200)
    score_posts = models.FloatField('项目分数',default=0.0)
    score_orders = models.FloatField('工单分数',default=0.0)
    score_cutovers = models.FloatField('割接分数',default=0.0)
    score_bonuses = models.FloatField('特殊加分',default=0.0)

    def __str__(self):
        return self.worker_name
    class Meta:
        verbose_name_plural = "总分"
        verbose_name = "总分排名"
