# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/1/29 20:43'

from .models import Teacher, CityDict, CourseOrg

import xadmin


class CityDictADmin(object):
	list_display = ['name', 'desc', 'add_time']
	search_fields = ['name', 'desc']
	list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
	list_display = ['name', 'fav_nums', 'click_nums', 'city', 'add_time']
	search_fields = ['name', 'fav_nums', 'click_nums', 'city']
	list_filter = ['name', 'fav_nums', 'click_nums', 'city__name', 'add_time']
	# # relfield_style = 'fk-ajax' # 有表以此为外键时，可以搜索
	relfield_style = 'fk-ajax'


class TeacherAdminAdmin(object):
	list_display = ['org', 'name', 'work_years', 'work_company', 'click_nums', 'add_time', 'add_time']
	search_fields = ['org', 'name', 'work_years', 'work_company', 'click_nums', 'add_time']
	list_filter = ['org__name', 'name', 'work_years', 'work_company', 'click_nums', 'add_time', 'add_time']


xadmin.site.register(CityDict, CityDictADmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdminAdmin)
