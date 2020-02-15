import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CityDict, CourseOrg, Teacher
from operation.models import UserAsk, UserFavorite
from courses.models import Course
from .forms import UserAskForm


# Create your views here.

class OrgListView(View):
	def get(self, request):
		all_citys = CityDict.objects.all()
		all_org = CourseOrg.objects.all()
		keywords = request.GET.get('keywords', '')

		# 搜索功能
		if keywords:
			all_org = all_org.filter(name__icontains=keywords)
		# 热门机构
		hot_org = all_org.order_by('-click_nums')[:3]
		# 机构类别
		category = request.GET.get('ct', '')
		if category and category is not None:
			all_org = all_org.filter(category=category)

		# 城市分类
		city_id = request.GET.get('city', '')
		if city_id and city_id is not None:
			city_id = int(city_id)
			all_org = all_org.filter(city=city_id)
		elif city_id is None:
			city_id = ''
		# 排序 按照课程数还是学习人数
		sort = request.GET.get('sort', '')
		if sort == 'students':
			all_org = all_org.order_by('-student_nums')
		elif sort == 'courses':
			all_org = all_org.order_by('-course_nums')
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		count = all_org.count()
		p = Paginator(all_org, 3, request=request)
		all_orgs = p.page(page)
		return render(request, 'org-list.html', {
			'all_citys': all_citys,
			'all_org': all_orgs,
			'sort': sort,
			'category': category,
			'city_id': city_id,
			'hot_org': hot_org,
			'count': count,
		})


class AddAskView(View):
	# 用户咨询
	def get(self, request):
		userAsk = UserAsk()
		userask_form = UserAskForm(request.POST)
		res = dict()
		if userask_form.is_valid():
			userAsk.name = request.POST.get('name', '')
			userAsk.mobile = request.POST.get('mobile', '')
			userAsk.course_name = request.POST.get('course_name', '')
			userAsk.save()

			res['status'] = 'success'
		else:
			res['status'] = 'fail'
			for key, errors in userask_form.errors.items():
				res['msg'] = errors
				break
		return HttpResponse(json.dumps(res), content_type='application/json')


class OrgHomeView(View):
	def get(self, request, org_id):
		hav_fav = False
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org_id):
				hav_fav = True
		status = 'home'
		org = CourseOrg.objects.get(id=org_id)
		org_teachers = org.teacher_set.all()[:4]
		org_course = org.course_set.all()[:5]
		return render(request, 'org-detail-homepage.html', {
			'org': org,
			'org_teachers': org_teachers,
			'org_course': org_course,
			'status': status,
			'hav_fav': hav_fav
		})


class OrgCourseView(View):
	def get(self, request, org_id):
		hav_fav = False
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org_id):
				hav_fav = True
		status = 'course'
		org = CourseOrg.objects.get(id=org_id)
		org_course = org.course_set.all()
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		count = org_course.count()
		p = Paginator(org_course, 1, request=request)
		org_courses = p.page(page)
		return render(request, 'org-detail-course.html', {
			'status': status,
			'org': org,
			'org_course': org_courses,
			'hav_fav': hav_fav
		})


class OrgDescView(View):
	def get(self, request, org_id):
		hav_fav = False
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org_id):
				hav_fav = True
		status = 'desc'
		org = CourseOrg.objects.get(id=org_id)
		return render(request, 'org-detail-desc.html', {
			'org': org,
			'status': status,
			'hav_fav': hav_fav
		})


class OrgTeachersView(View):
	def get(self, request, org_id):
		hav_fav = False
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org_id):
				hav_fav = True
		status = 'teacher'
		org = CourseOrg.objects.get(id=org_id)
		org_teacher = org.teacher_set.all()
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		count = org_teacher.count()
		p = Paginator(org_teacher, 1, request=request)
		org_teachers = p.page(page)
		return render(request, 'org-detail-teachers.html', {
			'status': status,
			'org': org,
			'org_teacher': org_teachers,
			'hav_fav': hav_fav
		})


class UserFavView(View):
	def ser_fav_data(self, fav_id, fav_type, sign):
		if fav_type == 1:  # 课程
			course = Course.objects.get(id=fav_id)
			course.fav_nums += sign
			if course.fav_nums < 0:
				course.fav_nums = 0
			course.save()
		if fav_type == 2:  # 机构
			Org = CourseOrg.objects.get(id=fav_id)
			Org.fav_nums += sign
			if Org.fav_nums < 0:
				Org.fav_nums = 0
			Org.save()
		if fav_type == 3:  # 讲师
			fav_tea = Teacher.objects.get(id=fav_id)
			fav_tea.fav_nums += sign
			if fav_tea.fav_nums < 0:
				fav_tea.fav_nums = 0
			fav_tea.save()

	def post(self, request):
		fav_id = int(request.POST.get('fav_id', 0))
		fav_type = int(request.POST.get('fav_type', 0))

		res = dict()

		if not request.user.is_authenticated:
			res['status'] = 'fail'
			res['msg'] = '用户未登陆'
			return HttpResponse(json.dumps(res), content_type='application/json')
		else:
			exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
			if exist_records:
				res['status'] = 'success'
				res['msg'] = '收藏'
				self.ser_fav_data(fav_id, fav_type, -1)
				exist_records.delete()
			else:
				user_fav = UserFavorite()
				if fav_type > 0 and fav_id > 0:
					res['status'] = 'success'
					res['msg'] = '已收藏'
					self.ser_fav_data(fav_id, fav_type, 1)

					user_fav.user = request.user
					user_fav.fav_type = fav_type
					user_fav.fav_id = fav_id
					user_fav.save()
				else:
					res['status'] = 'fail'
					res['msg'] = '收藏失败'
			return HttpResponse(json.dumps(res), content_type='application/json')


class TeacherListView(View):
	def get(self, request):
		teachers = Teacher.objects.all()
		hot_teachers = teachers.order_by('-click_nums')[:3]
		sort = request.GET.get('sort', '')
		keywords = request.GET.get('keywords', '')

		# 搜索功能
		if keywords:
			teachers = teachers.filter(name__icontains=keywords)

		if sort == 'count':
			teachers = teachers.order_by('-click_nums')
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		count = teachers.count()
		p = Paginator(teachers, 1, request=request)
		all_teachers = p.page(page)
		return render(request, 'teachers-list.html', {
			'teachers': all_teachers,
			'hot_teachers': hot_teachers,
			'count': count,
			'sort': sort
		})


class TeacherDetailView(View):
	def get(self, request, teacher_id):
		all_teachers = Teacher.objects.all()
		hot_teachers = all_teachers.order_by('-click_nums')[:3]
		teacher = Teacher.objects.get(id=teacher_id)
		course = Course.objects.filter(course_Teacher=teacher)
		# 收藏
		# 是否收藏
		hav_fav_teacher = False
		hav_fav_org = False

		if request.user.is_authenticated:  # is_authenticated是属性，不是方法
			if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
				hav_fav_teacher = True
		if request.user.is_authenticated:  # is_authenticated是属性，不是方法
			if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
				hav_fav_org = True
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		count = course.count()
		p = Paginator(course, 3, request=request)
		courses = p.page(page)
		return render(request, 'teacher-detail.html', {
			'teacher': teacher,
			'courses': courses,
			'hot_teachers':hot_teachers,
			'hav_fav_teacher':hav_fav_teacher,
			'hav_fav_org':hav_fav_org,
		})
