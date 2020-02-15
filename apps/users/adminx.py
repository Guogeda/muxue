# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/1/29 19:00'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import EmailVerfyRecode, Banner, UserProfile


class UserProflieAdmin(UserAdmin):
	pass


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True


class GlobalSettings(object):
	site_title = "宏杰后台管理系统"
	site_footer = "我的后台系统"
	menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
	list_display = ['code', 'email', 'type', 'send_time']
	search_fields = ['code', 'email', 'type']
	list_filter = ['code', 'email', 'type', 'send_time']


class BannerAdmin(object):
	list_display = ['title', 'image', 'url', 'index', 'add_time']
	search_fields = ['title', 'image', 'url', 'index']
	list_filter = ['title', 'image', 'url', 'index', 'add_time']


# from  django.contrib.auth.models import User
# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProflieAdmin)  /用userprofile代替user

xadmin.site.register(EmailVerfyRecode, EmailVerifyRecordAdmin)

xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
