# Generated by Django 2.1.2 on 2022-10-13 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20191222_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='body',
            field=models.TextField(default='', verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='orders_type',
            field=models.CharField(choices=[('行业', '行业'), ('物联网', '物联网'), ('内容计费', '内容计费'), ('DNS', 'DNS'), ('PCRF/PCF', 'PCRF/PCF'), ('国际漫游', '国际漫游'), ('SGSN/MME局数据', 'SGSN/MME局数据'), ('SGW/PGW局数据', 'SGW/PGW局数据'), ('AMF', 'AMF'), ('SMF', 'SMF'), ('NRF', 'NRF'), ('UPF', 'UPF'), ('数通', '数通'), ('网管', '网管'), ('I层', 'I层'), ('其他', '其他')], default='物联网', max_length=24, verbose_name='工单类型:'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_leader',
            field=models.CharField(choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员1'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_participant1',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员2'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_participant2',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员3'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_participant3',
            field=models.CharField(blank=True, choices=[('陈立栋', '陈立栋'), ('陈浚标', '陈浚标'), ('黄铭贤', '黄铭贤'), ('陆天洋', '陆天洋'), ('许海鹏', '许海鹏'), ('马梦阳', '马梦阳'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('彭俊霖', '彭俊霖'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨'), ('汪志武', '汪志武')], max_length=200, verbose_name='完成人员4'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pj_score',
            field=models.IntegerField(choices=[(0, 0), (1, 1)], default=1, verbose_name='工单加分'),
        ),
    ]
