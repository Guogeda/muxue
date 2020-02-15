# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/8 10:27'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """验证用户是否登录，如未登录转到登录页面"""
    @method_decorator(login_required(login_url='/users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)