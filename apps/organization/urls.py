# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/3 17:47'

from django.urls import path

from .views import OrgListView, AddAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeachersView, UserFavView, \
					TeacherListView, TeacherDetailView

urlpatterns = [
	# 机构url 管理
	path('list/', OrgListView.as_view(), name='org_list'),
	path('addask/', AddAskView.as_view(), name='add_ask'),
	path('org_home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
	path('org_course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
	path('org_desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
	path('org_teacher/<int:org_id>/', OrgTeachersView.as_view(), name='org_teacher'),
	path('add_fav/', UserFavView.as_view(), name='add_fav'),

	# 讲师url 管理
	path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
	path('teacher_detail/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail')
]
