"""muxue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve  # 处理静态文件
from django.conf.urls import url
from django.views.generic import TemplateView
import xadmin

from users.views import TestView, IndexView

urlpatterns = [

	path('xadmin/', xadmin.site.urls),
	path('test/', TestView.as_view(), name='test'),
	path("", IndexView.as_view(), name='index'),
	# 验证码路由
	path('captcha/', include('captcha.urls')),

	# 用户组
	path('users/', include(('users.urls', 'users'), namespace='users')),

	# 机构组路由
	path('org/', include(('organization.urls', 'organization'), namespace='org')),

	# 课程路由
	path('course/', include(('courses.urls', 'courses'), namespace='course')),

	# 富文本编辑器
	url(r'^ueditor/',include('DjangoUeditor.urls' )),

	# 静态文件路由
	url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]

if settings.DEBUG:
	urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))

# 全局页面配置
handler403 = 'users.views.page_not_look'
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
