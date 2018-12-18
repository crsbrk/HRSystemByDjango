# Generated by Django 2.1.2 on 2018-12-18 22:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20181118_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='is_delayed',
        ),
        migrations.AddField(
            model_name='orders',
            name='is_not_delayed',
            field=models.BooleanField(default=True, verbose_name='未超时'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='完成'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='orders_type',
            field=models.CharField(choices=[('行业', '行业'), ('物联网', '物联网'), ('内容计费', '内容计费'), ('DNS', 'DNS'), ('PCRF', 'PCRF'), ('国际漫游', '国际漫游'), ('SGSN/MME局数据', 'SGSN/MME局数据'), ('SGW/PGW局数据', 'SGW/PGW局数据'), ('其他', '其他')], default='物联网', max_length=24, verbose_name='工单类型:'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_leader',
            field=models.CharField(choices=[('陈立栋', '陈立栋'), ('常晓波', '常晓波'), ('刘江', '刘江'), ('刘雷', '刘雷'), ('刘峰', '刘峰'), ('冯庆', '冯庆'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('杨晓', '杨晓'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('韦国锐', '韦国锐'), ('张晨', '张晨')], max_length=200, verbose_name='完成人员1'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_participant1',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('常晓波', '常晓波'), ('刘江', '刘江'), ('刘雷', '刘雷'), ('刘峰', '刘峰'), ('冯庆', '冯庆'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('杨晓', '杨晓'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('韦国锐', '韦国锐'), ('张晨', '张晨')], max_length=200, verbose_name='完成人员2'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_participant2',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('常晓波', '常晓波'), ('刘江', '刘江'), ('刘雷', '刘雷'), ('刘峰', '刘峰'), ('冯庆', '冯庆'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('杨晓', '杨晓'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('韦国锐', '韦国锐'), ('张晨', '张晨')], max_length=200, verbose_name='完成人员3'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_participant3',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('常晓波', '常晓波'), ('刘江', '刘江'), ('刘雷', '刘雷'), ('刘峰', '刘峰'), ('冯庆', '冯庆'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('杨晓', '杨晓'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('韦国锐', '韦国锐'), ('张晨', '张晨')], max_length=200, verbose_name='完成人员4'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='workload_allot',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1)], verbose_name='比例1'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='workload_allot1',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1)], verbose_name='比例2'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='workload_allot2',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1)], verbose_name='比例3'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='workload_allot3',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1)], verbose_name='比例4'),
        ),
    ]
