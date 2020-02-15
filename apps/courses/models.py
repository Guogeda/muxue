# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


# Create your models here.

class Course(models.Model):
	tag = models.CharField(max_length=100, default='python', verbose_name='课程类别')
	course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, null=True, verbose_name='所属机构')
	course_Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, verbose_name='授课教师')
	name = models.CharField(max_length=50, verbose_name=u"课程名称")
	desc = UEditorField(verbose_name='课程详情', width=600, height=300, toolbars="full", imagePath="course/ueditor",
						  filePath="course/ueditor",
						  default='')
	detail = models.CharField(verbose_name='课程描述',max_length=200,default='')
	degree = models.CharField(choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), max_length=10,
							  verbose_name=u"课程难度")
	learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟)")
	students = models.IntegerField(default=0, verbose_name=u"学习人数")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
	image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面", default='default.png')
	click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
	need_know = models.CharField(max_length=300, default='', verbose_name='课程须知')
	tell_you = models.CharField(max_length=300, default='好好学习', verbose_name='老师告诉你什么')

	class Meta:
		verbose_name = u"课程"
		verbose_name_plural = verbose_name

	def get_lesson_nums(self):
		return self.lesson_set.count()

	get_lesson_nums.short_description = '章节数'

	def get_lesson(self):
		return self.lesson_set

	def __str__(self):
		return self.name


class BannerCourse(Course):
	class Meta:
		verbose_name = "轮播课程"
		verbose_name_plural = verbose_name
		proxy = True


class Lesson(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
	name = models.CharField(max_length=100, verbose_name=u"章节名")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"章节"
		verbose_name_plural = verbose_name

	def get_video(self):
		return self.video_set

	def __str__(self):
		return self.name


class Video(models.Model):
	Lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)
	name = models.CharField(max_length=100, verbose_name=u"视频名")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	file = models.FileField(upload_to='Video/%Y/%m', verbose_name='视频文件')
	url = models.CharField(default='', max_length=200, verbose_name='视频文件路径')

	class Meta:
		verbose_name = u"视频"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class CourseResource(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
	name = models.CharField(max_length=100, verbose_name=u"名称")
	download = models.FileField(upload_to="courses/resource/%Y/%m", verbose_name=u"资源下载")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"资源下载"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name
