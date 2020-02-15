# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/1/29 20:23'

import xadmin

from .models import Course, CourseResource, Lesson, Video, BannerCourse


class LessonInline(object):
	"""添加课程的时候可以顺便添加章节"""
	model = Lesson
	readonly_fields = ['add_time']
	extra = 0


class CourseResourceInline(object):
	"""添加课程的时候可以顺便添加课程资源"""
	model = CourseResource
	readonly_fields = ['add_time']
	extra = 0


class CourseResourceAdmin(object):
	list_display = ['course', 'name', 'download', 'add_time']
	search_fields = ['course', 'name', 'download']
	list_filter = ['course', 'name', 'download', 'add_time']
	model_icon = 'fa fa-free-code-camp'
	readonly_fields = ['add_time']


class CourseAdmin(object):
	list_display = ['name', 'degree', 'students', 'fav_nums', 'click_nums', 'add_time', 'get_lesson_nums']
	search_fields = ['name', 'degree', 'students', 'fav_nums', 'click_nums']
	list_filter = ['name', 'degree', 'students', 'fav_nums', 'click_nums', 'add_time', 'course_Teacher']
	readonly_fields = ['fav_nums', 'click_nums', 'students', 'add_time']
	# ordering = ['-click-nums']
	inlines = [LessonInline, CourseResourceInline]
	list_editable = ['degree']
	style_fields = {'detail':'ueditor',
					'desc':'ueditor'}
	import_excel = True

	def queryset(self):
		qs = super(CourseAdmin, self).queryset()
		qs = qs.filter(is_banner=False)
		return qs

	def save_models(self):
		"""在保存课程时，修改机构的课程总数"""
		obj = self.new_obj
		obj.save()
		if obj.course_org is not None:
			course_org = obj.course_org
			course_org.course_nums = Course.objects.filter(course_org=course_org).count()
			course_org.save()

	def post(self, request, *args, **kwargs):
		if 'excel' in request.FILES:
			pass
		return super(CourseAdmin, self).post(request, args, kwargs)


class BannercouseAdmin(object):
	list_display = ['name', 'degree', 'students', 'fav_nums', 'click_nums', 'add_time']
	search_fields = ['name', 'degree', 'students', 'fav_nums', 'click_nums']
	list_filter = ['name', 'degree', 'students', 'fav_nums', 'click_nums', 'add_time', 'course_Teacher']
	readonly_fields = ['fav_nums', 'click_nums', 'students', 'add_time']
	# ordering = ['-click-nums']
	inlines = [LessonInline, CourseResourceInline]

	def queryset(self):
		qs = super(BannercouseAdmin, self).queryset()
		qs = qs.filter(is_banner=True)
		return qs

	def save_models(self):
		"""在保存课程时，修改机构的课程总数"""
		obj = self.new_obj
		obj.save()
		if obj.course_org is not None:
			course_org = obj.course_org
			course_org.course_nums = Course.objects.filter(course_org=course_org).count()
			course_org.save()


class LessonAdmin(object):
	list_display = ['course', 'name', 'add_time']
	search_fields = ['course', 'name', ]
	list_filter = ['course__name', 'name', 'add_time']
	readonly_fields = ['add_time']


class VideoAdmin(object):
	list_display = ['Lesson', 'name', 'add_time']
	search_fields = ['Lesson', 'name', ]
	list_filter = ['Lesson__name', 'name', 'add_time']
	readonly_fields = ['add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannercouseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
