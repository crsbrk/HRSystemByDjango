from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from templates.constant_files import JOB_TYPES


ROLE_TYPES = (
    ('employee', '普通员工'),
    ('approver', '审批人'),
    ('manager', '管理员'),
)

WORK_APPLICATION_TYPES = (
    ('orders', '工单'),
    ('cutovers', '割接'),
    ('posts', '项目'),
    ('routine', '日常工作'),
    ('faulty', '故障处理'),
    ('bonuses', '特殊加分'),
)

WORK_APPLICATION_STATUS = (
    ('pending', '待审批'),
    ('approved', '已通过'),
    ('rejected', '已驳回'),
)


# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    profile_site = models.URLField("网站",blank=True)
    profile_phone = models.BigIntegerField("电话号码",blank=True)
    profile_job_type =  models.CharField("工作类型",choices=JOB_TYPES, max_length=50)
    role = models.CharField("角色", choices=ROLE_TYPES, max_length=20, default='employee')
    is_approved = models.BooleanField("账号已审批", default=False)
    profile_descption = models.TextField("个人介绍",blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField("照片",upload_to='profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

    @property
    def display_name(self):
        name = '%s%s' % (self.user.last_name, self.user.first_name)
        return name or self.user.get_full_name() or self.user.username

    @property
    def can_submit_work(self):
        return self.is_approved and not self.user.is_superuser


class SiteSetting(models.Model):
    project_name = models.CharField("项目名称", max_length=100, default='人力考核系统')
    footer_text = models.CharField("页脚名称", max_length=100, default='运维')
    logo = models.ImageField("导航栏Logo", upload_to='site_logo', blank=True)
    scores_announcement = models.TextField("考核原则公告（支持HTML）", blank=True, default='')
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "系统设置"
        verbose_name_plural = "系统设置"

    def __str__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HomeSlide(models.Model):
    title = models.CharField("标题", max_length=120, default='', blank=True)
    subtitle = models.CharField("副标题", max_length=240, default='', blank=True)
    image = models.ImageField("轮播图片", upload_to='home_slides')
    link = models.URLField("链接", default='', blank=True)
    sort_order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "首页轮播图"
        verbose_name_plural = "首页轮播图"
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title or self.image.name


class WorkApplication(models.Model):
    applicant = models.ForeignKey(User, verbose_name="申请人", on_delete=models.CASCADE, related_name='work_applications')
    work_type = models.CharField("申请类型", choices=WORK_APPLICATION_TYPES, max_length=20)
    title = models.CharField("标题", max_length=200)
    score = models.FloatField("申请分数", default=0)
    description = models.TextField("说明", default='', blank=True)
    evidence = models.FileField("证明材料", upload_to='work_evidence', blank=True)
    # 工单/割接编号
    work_num = models.CharField("编号", max_length=200, default='', blank=True)
    # 工单类型 / 故障类型
    work_subtype = models.CharField("子类型", max_length=100, default='', blank=True)
    # 厂家（故障处理用）
    work_manufacturer = models.CharField("厂家", max_length=100, default='', blank=True)
    # 截止/工作日期
    work_date = models.DateField("相关日期", null=True, blank=True)
    # 进度（项目用）
    work_progress = models.FloatField("当前进度", null=True, blank=True)
    # 完成人员1固定为申请人，这里记录申请人的完成比例。
    workload_allot = models.FloatField(
        "比例1", validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=1)
    pj_participant1 = models.CharField("完成人员2", max_length=200, default='', blank=True)
    workload_allot1 = models.FloatField(
        "比例2", validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0)
    pj_participant2 = models.CharField("完成人员3", max_length=200, default='', blank=True)
    workload_allot2 = models.FloatField(
        "比例3", validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0)
    pj_participant3 = models.CharField("完成人员4", max_length=200, default='', blank=True)
    workload_allot3 = models.FloatField(
        "比例4", validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0)
    status = models.CharField("状态", choices=WORK_APPLICATION_STATUS, max_length=20, default='pending')
    reviewer = models.ForeignKey(User, verbose_name="审批人", on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_work_applications')
    review_comment = models.TextField("审批意见", default='', blank=True)
    created_at = models.DateTimeField("提交时间", auto_now_add=True)
    reviewed_at = models.DateTimeField("审批时间", null=True, blank=True)
    materialized_model = models.CharField("生成业务表", max_length=30, default='', blank=True)
    materialized_object_id = models.PositiveIntegerField("生成业务ID", null=True, blank=True)

    class Meta:
        verbose_name = "工作量申请"
        verbose_name_plural = "工作量申请"
        ordering = ['-created_at']

    def __str__(self):
        return '%s - %s' % (self.applicant.username, self.title)
