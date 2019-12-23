from django.db import models
from django.contrib.auth.models import User
from templates.constant_files import JOB_TYPES



# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField("网站",blank=True)
    portfolio_phone = models.BigIntegerField("电话号码")
    portfolio_job_type =  models.CharField("工作类型",choices=JOB_TYPES, max_length=50)
    portfolio_descption = models.TextField("个人介绍")
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField("照片",upload_to='profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
