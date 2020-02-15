# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
	nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default='')
	birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
	gender = models.CharField(choices=(("male", u"男性"), ("female", u"女性")), default="female", max_length=7)
	address = models.CharField(max_length=100, default=u"")
	mobile = models.CharField(max_length=11, null=True, blank=True)
	image = models.ImageField(upload_to="image/%Y/%m", default='default.png', max_length=100)

	class Meta:
		verbose_name = "用户信息"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.username

	def get_unread_nums(self):
		"""获取未读消息数量"""
		from operation.models import UserMessage
		return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerfyRecode(models.Model):
	code = models.CharField(max_length=20, verbose_name=u"验证码")
	email = models.EmailField(max_length=50, verbose_name=u"邮箱")
	type = models.CharField(choices=(("register", u"注册"), ("forget", u"找回密码"),("update", u"重置密码")), max_length=20, verbose_name='验证码类型')
	send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")
	is_valid = models.BooleanField(default=False, verbose_name='是否有效')

	class Meta:
		verbose_name = u"邮箱验证码"
		verbose_name_plural = verbose_name

	def __str__(self):
		return '{0}({1})'.format(self.code, self.email)

	def get_send_time(self):
		return self.send_time


class Banner(models.Model):
	title = models.CharField(max_length=100, verbose_name=u"标题")
	image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u"轮播图", max_length=100)
	url = models.URLField(max_length=200, verbose_name=u"访问地址")
	index = models.IntegerField(default=100, verbose_name=u"顺序")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"访问时间")

	class Meta:
		verbose_name = u"轮播图"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.title
