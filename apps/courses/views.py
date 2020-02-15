import json

from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course, CourseResource, Video, Lesson
from operation.models import UserCourse, UserFavorite, CourseComment
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.

class CourseListView(View):
	def get(self, request):
		all_course = Course.objects.all()
		hot_course = all_course.order_by('-click_nums')[:3]
		sort = request.GET.get('sort', '')
		keywords = request.GET.get('keywords', '')
		# 搜索功能
		if keywords:
			all_course = all_course.filter(name__icontains=keywords)
		if sort == 'students':
			all_course = all_course.order_by('-students')
		elif sort == 'hot':
			all_course = all_course.order_by('-click_nums')
		# 分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		count = all_course.count()
		p = Paginator(all_course, 3, request=request)
		all_courses = p.page(page)
		return render(request, 'course-list.html', {
			'all_course': all_courses,
			'sort': sort,
			'hot_course': hot_course
		})


class CourseDetailView(View):
	def get(self, request, course_id):
		course = Course.objects.get(id=course_id)
		# 课程点击数
		course.click_nums += 1
		course.save()

		# 是否收藏
		hav_fav_course = False
		hav_fav_org = False

		if request.user.is_authenticated:  # is_authenticated是属性，不是方法
			if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course_id):
				hav_fav_course = True
		if request.user.is_authenticated:  # is_authenticated是属性，不是方法
			if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_id):
				hav_fav_org = True
		users = course.usercourse_set.filter(course_id=course_id)
		relate_course = Course.objects.filter(tag=course.tag)[:3]
		relate_courses = []
		for recourses in relate_course:
			if recourses.id != course.id:
				relate_courses.append(recourses)
		return render(request, 'course-detail.html', {
			'course': course,
			'users': users,
			'relate_course': relate_courses,
			'hav_fav_org': hav_fav_org,
			'hav_fav_course': hav_fav_course
		})


class CourseVideoView(LoginRequiredMixin, View):
	def get(self, request, course_id):
		course = Course.objects.get(id=course_id)
		all_lesson = course.get_lesson().all()
		resource = CourseResource.objects.get(id=course_id)

		# 课程学习人数
		course.students += 1
		course.save()

		# 学过该课程的同学还学过
		relate_students = UserCourse.objects.filter(course=course)
		student_id = [student.user.id for student in relate_students]
		relate_course = UserCourse.objects.filter(user__in=student_id)
		relate_course = [Course.objects.get(name=recourse.course) for recourse in relate_course]
		relate_courses = []
		for recourses in relate_course:
			if recourses.id != course.id:
				relate_courses.append(recourses)
		return render(request, 'course-video.html', {
			'course': course,
			'all_lesson': all_lesson,
			'resource': resource,
			'relate_courses': relate_courses[0:3],
		})


class CourseCommentView(LoginRequiredMixin, View):
	def get(self, request, course_id):
		course = Course.objects.get(id=course_id)
		resource = CourseResource.objects.get(id=course_id)
		comments = CourseComment.objects.filter(course=course)
		# 学过该课程的同学还学过
		relate_students = UserCourse.objects.filter(course=course)
		student_id = [student.user.id for student in relate_students]
		relate_course = UserCourse.objects.filter(user__in=student_id)
		relate_course = [Course.objects.get(name=recourse.course) for recourse in relate_course]
		relate_courses = []
		for recourses in relate_course:
			if recourses.id != course.id:
				relate_courses.append(recourses)

		return render(request, 'course-comment.html', {
			'course': course,
			'resource': resource,
			'relate_courses': relate_courses[0:3],
			'comments': comments
		})


class AddCommentView(View):
	def post(self, request):
		res = dict()
		course_id = int(request.POST.get('course_id', 0))
		course = Course.objects.get(id=course_id)
		comment = request.POST.get('comments', '')
		if not request.user.is_authenticated:
			res['status'] = 'fail'
			res['msg'] = '用户未登陆'
			return HttpResponse(json.dumps(res), content_type='application/json')
		else:
			if course_id > 0 and comment:
				CourCom = CourseComment()
				CourCom.course = course
				CourCom.user = request.user
				CourCom.comments = comment
				CourCom.save()

				res['status'] = 'success'
				res['msg'] = '评论成功'
			else:
				res['status'] = 'fail'
				res['msg'] = '发表评论失败'

			return HttpResponse(json.dumps(res), content_type='application/json')


class VideoPlayView(LoginRequiredMixin,View):
	def get(self, request, video_id):
		video = Video.objects.get(id=video_id)
		select_Lesson = Lesson.objects.get(id=video.Lesson.id)
		course = Course.objects.get(id=select_Lesson.course.id)
		course_id = course.id
		lessons = course.get_lesson().all()
		resource = CourseResource.objects.get(id=course_id)

		# 学过该课程的同学还学过
		relate_students = UserCourse.objects.filter(course=course)
		student_id = [student.user.id for student in relate_students]
		relate_course = UserCourse.objects.filter(user__in=student_id)
		relate_course = [Course.objects.get(name=recourse.course) for recourse in relate_course]
		relate_courses = []
		for recourses in relate_course:
			if recourses.id != course.id:
				relate_courses.append(recourses)

		return render(request, 'course-play.html', {
			'video': video,
			'course': course,
			'all_lesson': lessons,
			'resource': resource,
			'relate_courses': relate_courses[0:3],
		})
