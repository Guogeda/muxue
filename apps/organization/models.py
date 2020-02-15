# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models


# Create your models here.

class CityDict(models.Model):
	name = models.CharField(max_length=20, verbose_name=u"城市")
	desc = models.CharField(max_length=200, verbose_name=u"城市描述")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"城市"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class CourseOrg(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"机构名称")
	desc = models.CharField(max_length=100, verbose_name=u"机构描述")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
	image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=200)
	click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
	student_nums = models.IntegerField(default=0, verbose_name=u"学生数")
	course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
	address = models.CharField(max_length=100, verbose_name=u"机构地址")
	city = models.ForeignKey(CityDict, verbose_name=u"所在城市", on_delete=models.CASCADE)
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	category = models.CharField(max_length=10, choices=(('pxjg', u"培训机构"), ('gx', u"高校"), ('gr', u"个人")), default='pxjg'
								, verbose_name=u"机构类别")
	tag = models.CharField(max_length=5, default='全国知名' )

	class Meta:
		verbose_name = u"机构"
		verbose_name_plural = verbose_name

	def get_teacher_nums(self):
		return self.teacher_set.count()

	def get_course_nums(self):
		return self.course_set.count()

	def __str__(self):
		return self.name


class Teacher(models.Model):
	org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", on_delete=models.CASCADE)
	name = models.CharField(max_length=50, verbose_name=u"教师名")
	work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
	work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
	work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
	points = models.CharField(max_length=100, verbose_name=u"教学特点")
	click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
	course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
	image = models.ImageField(upload_to='Teachers/%Y/%m', default='default1.png', max_length=100, verbose_name='教师头像')
	olds = models.IntegerField(default=0, verbose_name='年龄')

	class Meta:
		verbose_name = u"教师"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

	def get_course_num(self):
		return self.course_set.all().count()
