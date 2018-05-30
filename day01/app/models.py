
from django.db import models

# Create your models here.

#创建模型


class Grades(models.Model):
    g_name = models.CharField(max_length=20)
    g_create_time = models.DateTimeField(auto_now_add=True)

    class Meta:#数据库中表格名称
        db_table = 'grade'


class Students(models.Model):
    s_name = models.CharField(max_length=20, null=False, unique=True)
    s_create_time = models.DateTimeField(auto_now_add=True)
    s_operate_time = models.DateTimeField(auto_now=True)
    s_img = models.ImageField(upload_to='upload', null=True)
    s_language = models.IntegerField(default=0)
    s_math = models.IntegerField(default=0)
    g = models.ForeignKey(Grades)

    class Meta:
        db_table = 'students'
