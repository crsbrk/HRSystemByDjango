# Generated by Django 2.1.2 on 2022-10-13 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faulty', '0007_auto_20200406_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faulty',
            name='pj_leader',
            field=models.CharField(choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员1'),
        ),
        migrations.AlterField(
            model_name='faulty',
            name='pj_manufacturer',
            field=models.CharField(choices=[('华为', '华为'), ('中兴', '中兴'), ('诺基亚', '诺基亚'), ('思科', '思科'), ('神州数码', '神州数码'), ('恒安嘉新', '恒安嘉新'), ('其他', '其他')], default='华为', max_length=200, verbose_name='厂家'),
        ),
        migrations.AlterField(
            model_name='faulty',
            name='pj_participant1',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员2'),
        ),
        migrations.AlterField(
            model_name='faulty',
            name='pj_participant2',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员3'),
        ),
        migrations.AlterField(
            model_name='faulty',
            name='pj_participant3',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员4'),
        ),
        migrations.AlterField(
            model_name='faulty',
            name='pj_score',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)], default=1, verbose_name='加分'),
        ),
        migrations.AlterField(
            model_name='faulty',
            name='pj_type',
            field=models.CharField(choices=[('硬件', '硬件'), ('软件', '软件'), ('投诉', '投诉'), ('其他', '其他')], default='硬件', max_length=200, verbose_name='故障类型'),
        ),
    ]
