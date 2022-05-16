from django.db import models
from rbac.models import User as rbacUser


# Create your models here.
class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(max_length=32, verbose_name='部门')

    def __str__(self):
        return self.title


class User(rbacUser):
    """
    用户表
    """
    phone = models.CharField(max_length=32, verbose_name='手机号')
    level_choices = (
        (1, 'T1'),
        (2, 'T2'),
        (3, 'T3'),
    )
    level = models.IntegerField(choices=level_choices, verbose_name='级别')
    depart = models.ForeignKey(to='Department', verbose_name='部门', on_delete=models.CASCADE)


class Host(models.Model):
    """
    主机表
    """
    hostname = models.CharField(max_length=32, verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='IP', protocol='both')
    depart = models.ForeignKey(to='Department', verbose_name='归属部门',on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname
