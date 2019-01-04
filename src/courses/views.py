from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from courses.models import Course, TeachersTeachCourses
from lectures.models import Lecture 
from datetime import datetime, timedelta


# Google AUTH
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Create your views here.

@csrf_exempt
def add_courses(request):
	if request.method == 'POST':
		token = request.META['HTTP_AUTHORIZATION']
		decoded_token = auth.verify_id_token(token)
		uid = decoded_token['uid']
		user = auth.get_user(uid)
		django_user, created = User.objects.get_or_create(email = 'sodhi@iitrpr.ac.in', defaults = {
			'username': 'balwinder',
			'password': 'iitropar',
		})
		profile = django_user.profile
		# Check if the user is a teacher
		if profile.is_teacher == False:
			return HttpResponseForbidden()

		teacher = profile.teacher

		days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
		
		course_json = request.POST # Body dekh lio kaise milti hai
		course, created = Course.objects.get_or_create(code = course_json['course_code'], defaults = {
			'name': course_json['course_name']})
		ttc, created = TeachersTeachCourses.objects.get_or_create(teacher = teacher, course = course)

		current_date = datetime.now()
		for weeks in range(16):
			# For 16 weeks
			# Get current week
			cur_week = current_date + timedelta(weeks = weeks)
			for days in range(5):
				# From monday to friday
				timing = course_json['lectures'][days_list[days]]
				# Get the days to add
				days_to_add = days - current_date.day
				days_to_add = days_to_add if days_to_add >=0 else 7 - days_to_add
				# Get the current day
				cur_day = cur_week + timedelta(days = days_to_add)

				for tim in timing:
					start_time = datetime.strptime(tim['start_time'], '%H:%M').time()
					end_time = datetime.strptime(tim['end_time'], '%H:%M').time()
					cur_start_datetime = datetime.combine(cur_day.date(), start_time)
					cur_end_datetime = datetime.combine(cur_day.date(), end_time)

					lecture, created = Lecture.objects.get_or_create(course = ttc, begin = cur_start_datetime, end = cur_end_datetime)

		return JsonResponse({"status": "Done"})
	 



