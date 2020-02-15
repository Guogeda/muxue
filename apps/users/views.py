# _*_ coding:utf-8 _*_
import json
from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import UserProfile, EmailVerfyRecode, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from .forms import LoginForm, RegisterForm, ForgetPWDForm, ModifyPWDForm, UploadImageForm, UpdateEmailForm, \
	UpUserInfoForm
from apps.utils.email_send import send_code_email
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class TestView(View):
	def get(self, request):
		return render(request, '', context='dwdwwdwd')


class CustomBackend(ModelBackend):
	# 重写 authenticate 方法，邮箱也可以登陆,在setting 中先声明
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))
			if user.check_password(password):
				return user
			else:
				return None
		except Exception as e:
			return None


class LoginView(View):
	def get(self, request):
		return render(request, 'login.html', {})

	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user_name = request.POST.get('username', '')
			pass_word = request.POST.get('password', '')
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('index'))
				else:
					return render(request, 'login.html', {
						'msg': '用户未激活'
					})
			else:
				return render(request, 'login.html', {'msg': '用户名密码错误'})
		else:
			return render(request, 'login.html', {
				'login_form': login_form
			})


class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html', {'register_form': register_form})

	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			email = request.POST.get('email', '')
			password = request.POST.get('password', '')
			if UserProfile.objects.filter(email=email):
				return render(request, 'register.html', {
					'msg': u'该邮箱已被注册',
					'register_form': register_form
				})
			else:
				user_profile = UserProfile()
				user_profile.username = email
				user_profile.email = email
				user_profile.password = make_password(password)
				user_profile.is_active = False
				user_profile.save()

				try:
					send_code_email(email, send_type='register')
				except AttributeError:
					return render(request, 'register.html', {
						'msg': '邮箱错误'
					})
				return render(request, 'email_send_success.html', {
					'msg': '请前往查收并尽快激活账户',
					'email': email
				})
		else:
			return render(request, 'register.html', {
				'register_form': register_form,
				'msg': ''
			})


class RegisterActiveView(View):
	def get(self, request, url_active_code):
		register_actives = EmailVerfyRecode.objects.filter(code=url_active_code, is_valid=0)
		if register_actives:
			for register_active in register_actives:
				email = register_active.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
				register_active.is_valid = 1
				register_active.save()
				return render(request, 'register_active_success.html', {})
		else:
			return render(request, 'register_active_failed.html', {})


class ForgetpwdView(View):
	# 忘记密码并发送邮箱
	def get(self, request):
		ForgetPwd_Form = ForgetPWDForm()
		return render(request, 'forgetpwd.html', {
			'ForgetPwd_Form': ForgetPwd_Form
		})

	def post(self, request):
		ForgetPwd_Form = ForgetPWDForm(request.POST)
		email = request.POST.get('email', '')
		if ForgetPwd_Form.is_valid():
			if UserProfile.objects.filter(email=email):
				try:
					send_code_email(email, send_type='forget')
				except AttributeError:
					return render(request, 'forgetpwd.html', {
						'msg': '邮箱错误'
					})
				return render(request, 'email_send_success.html', {
					'msg': '请前往查收并尽快激活重置密码链接',
					'email': email
				})
			else:
				return render(request, 'forgetpwd.html', {
					'msg': '该用户未注册，请注册'
				})
		else:
			return render(request, 'forgetpwd.html', {
				'ForgetPwd_Form': ForgetPwd_Form
			})


class ResetPsdView(View):
	def get(self, request, url_reset_code):
		reset_actives = EmailVerfyRecode.objects.filter(code=url_reset_code, is_valid=0)
		if reset_actives:
			for reset_active in reset_actives:
				return render(request, 'password_reset.html', {
					'email': reset_active.email,
					'url_reset_code': url_reset_code
				})
		else:
			return render(request, 'test.html', {})


class ModifyPsdView(View):
	# def get(self, request):
	# 	return render(request, 'password_reset.html', {})
	def post(self, request):
		modify_form = ModifyPWDForm(request.POST)
		if modify_form.is_valid():
			password1 = request.POST.get('password1', '')
			password2 = request.POST.get('password2', '')
			email = request.POST.get('email', '')
			url_reset_code = request.POST.get('url_reset_code', '')
			if password1 == password2:
				user = UserProfile.objects.get(email=email)
				user.password = make_password(password1)
				user.save()

				modify_pwds = EmailVerfyRecode.objects.filter(code=url_reset_code)
				for modify_pwd in modify_pwds:
					modify_pwd.is_valid = 1
					modify_pwd.save()
				return render(request, 'login.html', {
					'msg': '密码重置成功，请登陆'
				})
			else:
				return render(request, 'password_reset.html', {
					'msg': '两次密码输入不一致'
				})

		else:
			return render(request, 'password_reset.html', {
				'modify_form': modify_form
			})


class UserInfoView(LoginRequiredMixin, View):
	def get(self, request):
		# 前端左侧列表显示
		state = 'info'
		# user = UserProfile.objects.get(id=request.user.id)
		return render(request, 'usercenter-info.html', {
			'state': state
		})


class UploadImageView(LoginRequiredMixin, View):
	# 修改头像
	def post(self, request):
		res = dict()
		image = UploadImageForm(request.POST, request.FILES, instance=request.user)
		if image.is_valid():
			image.save()
			res['status'] = 'success'
			res['msg'] = '头像修改成功'
		else:
			res['status'] = 'fail'
			res['msg'] = '头像修改失败'
		return HttpResponse(json.dumps(res), content_type='application/json')


class UpdatePwdView(View):
	# 修改密码
	def post(self, request):
		updatepwd_form = ModifyPWDForm(request.POST)
		res = dict()
		if updatepwd_form.is_valid():
			pwd1 = request.POST.get('password1', '')
			pwd2 = request.POST.get('password2', '')
			if pwd1 != pwd2:
				res['status'] = 'fail'
				res['msg'] = '两次密码不一致'
				return HttpResponse(json.dumps(res), content_type='application/json')

			user = request.user
			user.password = make_password(pwd2)
			user.save()

			res['status'] = 'success'
			res['msg'] = '密码修改成功'
		else:
			res = updatepwd_form.errors
		return HttpResponse(json.dumps(res), content_type='application/json')


class UpdateEmailView(View):
	# 修改邮箱
	# 邮箱 model 中的 is_vaild 命名错误，应为 is_used
	def post(self, request):
		update_email_form = UpdateEmailForm(request.POST)
		res = dict()
		if update_email_form.is_valid():
			email = request.POST.get('email', '')
			code = request.POST.get('code', '')
			exit_email = EmailVerfyRecode.objects.get(type='update', code=code, email=email, is_valid=0)
			now_time = datetime.now()
			send_times = exit_email.get_send_time()
			if exit_email:
				if (now_time - send_times).seconds > 60:
					exit_email.is_valid = 0
					exit_email.save()
					res['status'] = 'fail'
					res['msg'] = '验证码失效，请输入最新验证码'
				else:
					exit_email.is_valid = 0
					exit_email.save()

					User = request.user
					User.email = email
					User.save()
					res['status'] = 'success'
					res['msg'] = '密码修改成功'
			else:
				res['status'] = 'fail'
				res['msg'] = '验证码错误，请输入最新验证码'
		else:
			res['status'] = 'fail'
			res['msg'] = '邮箱发送失败'
		return HttpResponse(json.dumps(res), content_type='application/json')


class SendEmailCodeView(View):
	# 给修改邮箱发送验证码
	def get(self, request):
		email = request.GET.get('email', '')
		res = dict()
		exist_emails = EmailVerfyRecode.objects.filter(email=email, type='update', is_valid=0)
		if exist_emails:
			for exist_email in exist_emails:
				exist_email.is_valid = 1
				exist_email.save()
		if email:
			if UserProfile.objects.filter(email=email):
				res['status'] = 'failure'
				res['msg'] = '该邮箱已被注册'
			else:
				try:
					send_code_email(email, send_type='update')
					res['status'] = 'success'
				except AttributeError:
					res['status'] = 'failure'
					res['msg'] = '邮箱发送失败'
		return HttpResponse(json.dumps(res), content_type='application/json')


class UpdateUserProfileView(View):
	# 修改个人信息
	def post(self, request):
		user_form = UpUserInfoForm(request.POST, instance=request.user)
		res = dict()
		if user_form.is_valid():
			user_form.save()
			res['status'] = 'success'
		else:
			res = user_form.errors
		return HttpResponse(json.dumps(res), content_type='application/json')


class MycourseView(View):
	# 个人中心 -我的课程显示
	def get(self, request):
		state = 'course'
		course = UserCourse.objects.filter(user=request.user)
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(course, 3, request=request)
		courses = p.page(page)
		return render(request, 'usercenter-mycourse.html', {
			'state': state,
			'courses': courses
		})


class MyFavOrgView(View):
	# 个人中心- 我的收藏 课程机构
	def get(self, request):
		state = 'fav'
		fav_org_list_id = UserFavorite.objects.filter(user=request.user, fav_type=2)
		fav_org_list = [CourseOrg.objects.get(id=org_id.fav_id) for org_id in fav_org_list_id]
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(fav_org_list, 3, request=request)
		fav_orgs = p.page(page)
		return render(request, 'usercenter-fav-org.html', {
			'state': state,
			'fav_orgs': fav_orgs
		})


class MyFavCourseView(View):
	# 个人中心- 我的收藏 课程
	def get(self, request):
		state = 'fav'
		fav_course_list_id = UserFavorite.objects.filter(user=request.user, fav_type=1)
		fav_course_list = [Course.objects.get(id=course_id.fav_id) for course_id in fav_course_list_id]
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(fav_course_list, 3, request=request)
		fav_courses = p.page(page)
		return render(request, 'usercenter-fav-course.html', {
			'state': state,
			'fav_courses': fav_courses
		})


class MyFavTeacherView(View):
	# 个人中心 - 我的收藏， 教师
	def get(self, request):
		state = 'fav'
		fav_teacher_list_id = UserFavorite.objects.filter(user=request.user, fav_type=3)
		fav_teacher_list = [Teacher.objects.get(id=teacher_id.fav_id) for teacher_id in fav_teacher_list_id]
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(fav_teacher_list, 3, request=request)
		fav_teachers = p.page(page)
		return render(request, 'usercenter-fav-teacher.html', {
			'state': state,
			'fav_teachers': fav_teachers
		})


class UserMessageView(View):
	# 用户消息
	def get(self, request):
		state = 'msg'
		messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
		for message in messages:
			message.has_read = True
			message.save()

		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(messages, 3, request=request)
		messages = p.page(page)
		return render(request, 'usercenter-message.html', {
			'state': state,
			'messages': messages,
		})


class LogoutView(View):
	"""注销登录功能"""

	def get(self, request):
		logout(request)
		return HttpResponseRedirect(reverse('index'))


class IndexView(View):
	def get(self, request):
		banners = Banner.objects.all()
		banner_course = Course.objects.filter(is_banner=True)
		courses = Course.objects.filter(is_banner=False)
		org = CourseOrg.objects.all()
		return render(request, 'index.html', {
			'banners': banners,
			'banner_course': banner_course,
			'courses': courses,
			'orgs': org
		})


def page_not_look(request, exception):
	"""全局403配置"""
	from django.shortcuts import render_to_response
	response = render_to_response('403.html', {})
	response.status_code = 403
	return response


def page_not_found(request, exception):
	"""全局404配置"""
	from django.shortcuts import render_to_response
	response = render_to_response('404.html', {})
	response.status_code = 404
	return response


def page_error(request, exception):
	"""全局500配置"""
	from django.shortcuts import render_to_response
	response = render_to_response('500.html', {})
	response.status_code = 500
	return response
