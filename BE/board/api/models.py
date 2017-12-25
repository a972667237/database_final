#coding:utf-8
from django.db import models

oriType = (
    (u'教务', u'教学教务'),
    (u'学术', u'学术科研'),
    (u'行政', u'行政通知'),
    (u'学工', u'学生工作'),
    (u'校园', u'校园生活')
)
# Create your models here.
class Announce(models.Model):
    s_type = models.ForeignKey('SType',on_delete=models.CASCADE, null=True)
    ori_type = models.CharField(u"原始类别", max_length=4, choices=oriType)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    title = models.CharField(u"标题",max_length=100)
    content = models.TextField(u"内容", max_length=2000)
    time = models.TimeField(u"发文时间", auto_created=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "公文"
        verbose_name_plural = verbose_name

class SType(models.Model):
    name = models.CharField(u"类名", max_length=10)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "小类"
        verbose_name_plural = verbose_name

class Unit(models.Model):
    name = models.CharField(u"单位名", max_length=50)
    user = models.CharField(u'英文名', max_length=50, null=True)
    perm = models.IntegerField(u"权限等级")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "单位"
        verbose_name_plural = verbose_name

class Show(models.Model):
    isTop = models.BooleanField(u"置顶", default=False)
    isShow = models.BooleanField(u"继续展示", default=False)
    click = models.IntegerField(u"点击量", default=0)
    approve = models.IntegerField(u"点赞量", default=0)
    announce = models.OneToOneField('Announce', on_delete=models.CASCADE)
    def __str__(self):
        return self.announce.title
    class Meta:
        verbose_name = "已展示公文"
        verbose_name_plural = verbose_name

class AFile(models.Model):
    aid = models.ForeignKey('Announce', on_delete=models.CASCADE)
    link = models.URLField(u"下载链接")
    def __str__(self):
        return self.aid
    class Meta:
        verbose_name = "公文文件"
        verbose_name_plural = verbose_name
