# Generated by Django 2.1.2 on 2018-12-25 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cutovers', '0003_auto_20181218_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cutovers',
            name='pj_leader',
            field=models.CharField(choices=[('陈立栋', '陈立栋'), ('常晓波', '常晓波'), ('刘江', '刘江'), ('刘雷', '刘雷'), ('刘峰', '刘峰'), ('冯庆', '冯庆'), ('郭少钏', '郭少钏'), ('于秋思', '于秋思'), ('苏飓', '苏飓'), ('苏伟衡', '苏伟衡'), ('杨晓', '杨晓'), ('霍晓歌', '霍晓歌'), ('李晓昕', '李晓昕'), ('张晨', '张晨')], max_length=200, verbose_name='割接负责人'),
        ),
    ]
