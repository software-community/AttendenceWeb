from django.conf import settings
from rest_framework import serializers
from django.core import serializers as dserializers
from .models import Profile, Student, Teacher, StudentImage
from courses.models import TeachersTeachCourses, StudentAttendCourses

import datetime
from lectures.models import Lecture, StudentsAttendLectures

from django.db.models import F
from django.db.models import Count
from django.db.models.functions import TruncTime


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):

	courses = serializers.SerializerMethodField()
	lecture_done = serializers.SerializerMethodField()
	lecture_pending = serializers.SerializerMethodField()

	class Meta:
		model = Student
		fields = '__all__'

	def get_courses(self, instance):
		"""
		Gets the list of courses the student is enrolled in
		"""
		queryset = [sac.course for sac in StudentAttendCourses.objects.filter(student = instance)]
		print(queryset)
		queryset = [{ 'id': item.id, \
		'attendace':(self.get_attendance(item.id, instance)),\
		'code': item.course.code} for item in queryset]
		return queryset

	def get_lecture_done(self, instance):
		"""
		Gets the lectures that are today with attendance status
		"""
		today_time = datetime.datetime.now() 
		today = datetime.datetime.now().date()

		lectures = Lecture.objects.all().filter(begin__date = today, begin__lte = today_time)
		queryset = StudentsAttendLectures.objects.filter(student = instance, lecture__in = lectures).annotate(time = TruncTime('lecture__begin')).values('id', 'lecture', 'present', 'time', course_id = F('lecture__course'), code = F('lecture__course__course__code'))
		return list(queryset)

	def get_lecture_pending(self, instance):
		"""
		Gets the lectures that are today with attendance status
		"""
		today_time = datetime.datetime.now() 
		today = datetime.datetime.now().date()
		lectures = Lecture.objects.all().filter(begin__date = today, begin__gt = today_time)
		queryset = StudentsAttendLectures.objects.filter(student = instance, lecture__in = lectures).annotate(time = TruncTime('lecture__begin')).values('id', 'lecture', 'present', 'time', course_id = F('lecture__course'), code = F('lecture__course__course__code'))
		return list(queryset)

	def get_attendance(self, course_id, instance):
		"""
		Calculates the attendance of the student in a course
		"""
		today = datetime.datetime.now().date()
		lectures = Lecture.objects.all().filter(course__id =course_id, begin__date__lte = today)
		att = StudentsAttendLectures.objects.filter(student = instance, lecture__in = lectures).values('present')

		total_att = 0
		for att_status in att:
			total_att += int(att_status['present'])

		return total_att*1.0/len(att) if len(att) > 0 else 0.0


class StudentImageSerializer(serializers.ModelSerializer):

	class Meta:
		model = StudentImage
		fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
	courses = serializers.SerializerMethodField()
	lecture_done = serializers.SerializerMethodField()
	lecture_pending = serializers.SerializerMethodField()

	class Meta:
		model = Teacher
		fields = '__all__'

	def get_courses(self, instance):
		"""
		Gets the list of courses the student is enrolled in
		"""
		queryset = list(TeachersTeachCourses.objects.filter(teacher = instance).values('id', 'course__code', 'course__name', 'student_code', 'ta_code').annotate(students_count=Count('students')))
		# queryset = [{
		# 'id': item['id'],
		# 'course_code': item['course__code'],
		# } for item in queryset]
		return queryset

	def get_lecture_done(self, instance):
		"""
		Gets the lectures that are today with attendance status
		"""
		today_time = datetime.datetime.now() 
		today = datetime.datetime.now().date()

		lectures = Lecture.objects.all().filter(begin__date = today, begin__lte = today_time).annotate(time = TruncTime('begin')).values('id', 'time', 'course', code = F('course__course__code'))
		return list(lectures)


	def get_lecture_pending(self, instance):
		"""
		Gets the lectures that are today with attendance status
		"""
		today_time = datetime.datetime.now() 
		today = datetime.datetime.now().date()
		lectures = Lecture.objects.all().filter(begin__date = today, begin__gt = today_time).annotate(time = TruncTime('begin')).values('id', 'time', 'course', code = F('course__course__code'))
		return list(lectures)