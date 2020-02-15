# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course


# Create your models here.

class UserAsk(models.Model):
	# 我要报名
	name = models.CharField(max_length=20, verbose_name=u"姓名")
	mobile = models.CharField(max_length=11, verbose_name=u"手机")
	course_name = models.CharField(max_length=50, verbose_name=u"课程名")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"用户咨询"
		verbose_name_plural = verbose_name


class CourseComment(models.Model):
	# 课程评论
	user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
	course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
	comments = models.CharField(max_length=200, verbose_name=u"评论内容")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"课程评论"
		verbose_name_plural = verbose_name


class UserFavorite(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
	fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
	fav_type = models.CharField(choices=((1, "课程"), (2, "课程机构"), (3, "教师")), verbose_name=u"收藏种类", max_length=10)
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"用户收藏"
		verbose_name_plural = verbose_name


class UserMessage(models.Model):
	# user = models.ForeignKey(UserProfile, verbose_name=u"用户") :不用外键，消息用种类时发给所有用户还是指定用户
	user = models.IntegerField(default=0, verbose_name=u"接收用户")
	message = models.CharField(max_length=500, verbose_name=u"消息内容")
	has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"用户消息"
		verbose_name_plural = verbose_name


class UserCourse(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
	course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"用户课程"
		verbose_name_plural = verbose_name

	def __str__(self):
		return "{}添加{}".format(self.user, self.course)
