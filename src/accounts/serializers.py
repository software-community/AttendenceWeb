from django.conf import settings
from rest_framework import serializers
from django.core import serializers as dserializers
from .models import Profile, Student, Teacher
from courses.models import TeachersTeachCourses

import datetime
from lectures.models import Lecture, StudentsAttendLectures


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):

	courses = serializers.SerializerMethodField()
	lecture_today = serializers.SerializerMethodField()

	class Meta:
		model = Student
		fields = '__all__'

	def get_courses(self, instance):
		"""
		Gets the list of courses the student is enrolled in
		"""
		queryset = list(TeachersTeachCourses.objects.filter(students = instance).values('id'))
		queryset = [{ 'id': item['id'], 'attendace':(self.get_attendance(item['id'], instance))} for item in queryset]
		return queryset

	def get_lecture_today(self, instance):
		"""
		Gets the lectures that are today with attendance status
		"""
		today = datetime.datetime.now().date()
		lectures = Lecture.objects.all().filter(begin__date = today)
		queryset = StudentsAttendLectures.objects.filter(student = instance, lecture__in = lectures).values('id', 'lecture', 'present', 'lecture__course')
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





class TeacherSerializer(serializers.ModelSerializer):
	courses = serializers.SerializerMethodField()
	lecture_today = serializers.SerializerMethodField()

	class Meta:
		model = Teacher
		fields = '__all__'

	def get_courses(self, instance):
		"""
		Gets the list of courses the student is enrolled in
		"""
		queryset = list(TeachersTeachCourses.objects.filter(teacher = instance).values('id'))
		queryset = [item['id'] for item in queryset]
		return queryset

	def get_lecture_today(self, instance):
		"""
		Gets the lectures that are today with attendance status
		"""
		today = datetime.datetime.now().date()
		queryset = Lecture.objects.all().filter(begin__date = today, course__teacher = instance).values('id', 'course')
		return list(queryset)