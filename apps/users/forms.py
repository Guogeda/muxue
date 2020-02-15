# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/1/31 15:24'

from django import forms

from captcha.fields import CaptchaField
from .models import UserProfile



class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=5)
	captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetPWDForm(forms.Form):
	email = forms.EmailField(required=True)
	captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPWDForm(forms.Form):
	password1 = forms.CharField(required=True, min_length=5)
	password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
	# 修改个人头像
	class Meta:
		model = UserProfile
		fields = ['image']


class UpdateEmailForm(forms.Form):
	email = forms.EmailField(required=True)
	code = forms.CharField(required=True, max_length=4)


class UpUserInfoForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']