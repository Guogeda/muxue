# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/6 14:28'

from django.urls import path
from .views import CourseListView, CourseDetailView, CourseCommentView, CourseVideoView, AddCommentView, VideoPlayView

urlpatterns = [
	path('list/', CourseListView.as_view(), name='course_list'),
	path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
	path('info/<int:course_id>/', CourseVideoView.as_view(), name='course_info'),
	path('comment/<int:course_id>/', CourseCommentView.as_view(), name='course_comment'),
	path('video/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),
	path('add_comment/', AddCommentView.as_view(), name='add_comment'),

]
