# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/3 10:50'

from django.urls import path

from .views import LoginView, LogoutView, RegisterView, RegisterActiveView, ResetPsdView, ForgetpwdView, ModifyPsdView
from .views import UserInfoView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, UpdateUserProfileView , UploadImageView
from .views import MycourseView, MyFavOrgView, MyFavCourseView, MyFavTeacherView, UserMessageView

urlpatterns = [
	path("login/", LoginView.as_view(), name='login'),
	path("logout/", LogoutView.as_view(), name='logout'),
	path("register/", RegisterView.as_view(), name='register'),
	path('active/<url_active_code>', RegisterActiveView.as_view(), name='register_active'),
	path('reset/<url_reset_code>', ResetPsdView.as_view(), name='resetpwd'),
	path('forgetpwd/', ForgetpwdView.as_view(), name='forgetpwd'),
	path('modifypwd/', ModifyPsdView.as_view(), name='modifypwd'),
	# 个人中心-个人信息页
	path('info/', UserInfoView.as_view(), name='user_info'),
	path('image/upload/', UploadImageView.as_view(), name='user_upload_image'),
	path('update/pwd/', UpdatePwdView.as_view(), name='user_update_pwd'),
	path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
	path('update_email/', UpdateEmailView.as_view(), name='user_update_email'),
	path('updatepro/', UpdateUserProfileView.as_view(), name='user_update_profile'),
	# 个人中心 -我的课程
	path('course/', MycourseView.as_view(), name='user_course'),
	# 个人中心- 我的收藏
	path('fav_org/', MyFavOrgView.as_view(), name='user_fav_org'),
	path('fav_course/', MyFavCourseView.as_view(), name='user_fav_course'),
	path('fav_teacher/', MyFavTeacherView.as_view(), name='user_fav_teacher'),
	# 个人中心 - 我的消息
	path('my_message/', UserMessageView.as_view(), name='user_message'),
]
