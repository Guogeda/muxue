# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/1/29 20:52'

from .models import UserAsk, CourseComment, UserFavorite, UserMessage, UserCourse
import xadmin


class UserAskAdmin(object):
	list_display = ['name', 'mobile', 'course_name', 'add_time']
	search_fields = ['name', 'mobile', 'course_name']
	list_filter = ['name', 'mobile', 'course_name', 'add_time']
	model_icon = 'fa fa-question-circle'


class CourseCommentAdmin(object):
	list_display = ['user', 'course', 'comments', 'add_time']
	search_fields = ['user', 'course', 'comments']
	list_filter = ['user__nick_name', 'course__name', 'comments', 'add_time']
	model_icon = 'fa fa-comments'


class UserFavoriteAdmin(object):
	list_display = ['user', 'fav_id', 'fav_type', 'add_time']
	search_fields = ['user', 'fav_id', 'fav_type']
	list_filter = ['user__nick_name', 'fav_id', 'fav_type', 'add_time']
	model_icon = 'fa fa-star'


class UserMessageAdmin(object):
	list_display = ['user', 'message', 'has_read', 'add_time']
	search_fields = ['user', 'message', 'has_read']
	list_filter = ['user', 'message', 'has_read', 'add_time']
	model_icon = 'fa fa-commenting'



class UserCourseAdmin(object):
	list_display = ['user', 'course', 'add_time']
	search_fields = ['user', 'course']
	list_filter = ['user__nick_name', 'course', 'add_time']
	model_icon = 'fa fa-leanpub'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
