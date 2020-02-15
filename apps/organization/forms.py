# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/4 20:22'
import re

from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
	class Meta:
		model = UserAsk
		fields = ['name', 'mobile', 'course_name']

	def clean_mobile(self):
		mobile = self.cleaned_data['mobile']
		p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
		if p.match(mobile):
			return mobile
		raise forms.ValidationError('手机号码格式不正确', code='mobile_inval')