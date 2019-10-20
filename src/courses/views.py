from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from courses.models import Course, TeachersTeachCourses, StudentAttendCourses
from lectures.models import Lecture
from accounts.models import Profile


# Google AUTH
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Create your views here.
import json


@csrf_exempt
def add_courses(request):
    if request.method == 'POST':
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            django_user = User.objects.get(email=user.email)
            profile = Profile.objects.get(user=django_user, is_teacher=True)

            teacher = profile.teacher

            days_list = ['monday', 'tuesday', 'wednesday',
                         'thursday', 'friday', 'saturday', 'sunday']

            course_json = request.body.decode('utf-8')
            course_json = json.loads(course_json)
            course, created = Course.objects.get_or_create(code=course_json['course_code'].upper(), defaults={
                'name': course_json['course_name']})
            ttc, created = TeachersTeachCourses.objects.get_or_create(
                teacher=teacher, course=course)

            start_date = datetime.strptime(
                course_json['start_date'][:10], '%Y-%m-%d').date()
            end_date = datetime.strptime(
                course_json['end_date'][:10], '%Y-%m-%d').date()

            delta = timedelta(days=1)
            while start_date <= end_date:
                timing = course_json['lectures'][days_list[start_date.weekday()]]
                for tim in timing:
                    start_time = datetime.strptime(
                        tim['start_time'], '%H:%M').time()
                    end_time = datetime.strptime(
                        tim['end_time'], '%H:%M').time()
                    cur_start_datetime = datetime.combine(
                        start_date, start_time)
                    cur_end_datetime = datetime.combine(start_date, end_time)

                    lecture, created = Lecture.objects.get_or_create(
                        course=ttc, begin=make_aware(cur_start_datetime),
                        end=make_aware(cur_end_datetime), lecture_type=tim['type'])

                start_date += delta

            return JsonResponse({"status": "ok", "student_code": ttc.student_code, "ta_code": ttc.ta_code})
        except Exception as err:
            print(err)
            return JsonResponse({'status': 'Fail'})


@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        # print(request.META['HTTP_AUTHORIZATION'])
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            # display_name = user.displayName.split(" ")
            django_user = User.objects.get(email=user.email)
            if django_user.profile.is_student:
                student = django_user.profile.student
                course_json = json.loads(request.body.decode('utf-8'))
                code = course_json['code']
                course = TeachersTeachCourses.objects.get(student_code=code)
                StudentAttendCourses.objects.create(
                    student=student, course=course)

            return JsonResponse({'status': 'Success'})
        except:
            return JsonResponse({'status': 'Fail'})

    else:
        return JsonResponse({'status': 'Fail'})


@csrf_exempt
def add_ta(request):
    if request.method == 'POST':
        # print(request.META['HTTP_AUTHORIZATION'])
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            # display_name = user.displayName.split(" ")
            django_user = User.objects.get(email=user.email)
            if django_user.profile.is_teacher:
                teacher = django_user.profile.teacher
                course_json = json.loads(request.body.decode('utf-8'))
                code = course_json['code']
                course = TeachersTeachCourses.objects.get(ta_code=code)
                course.teaching_assistants.add(teacher)

            return JsonResponse({'status': 'Success'})
        except:
            return JsonResponse({'status': 'Fail'})

    else:
        return JsonResponse({'status': 'Fail'})
