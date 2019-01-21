from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from .models import Course, TeachersTeachCourses
from lectures.permissions import WriteTokenOnly

from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.filters import SearchFilter
from rest_condition import Or


from .serializers import CourseSerializer, TeachersTeachCoursesSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from lectures.models import Lecture, StudentsAttendLectures

class CourseViewSet(viewsets.ModelViewSet):
	
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (Or(permissions.IsAdminUser, WriteTokenOnly),)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('name', 'teachers', )

class TeachersTeachCoursesViewSet(viewsets.ModelViewSet):
	
	queryset = TeachersTeachCourses.objects.all()
	serializer_class = TeachersTeachCoursesSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (Or(permissions.IsAdminUser, WriteTokenOnly),)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('teacher', 'course', 'students', 'teaching_assistants')
	search_fields = ('teacher__user__first_name', 'teacher__user__last_name')


class StudentAttendance(APIView):

	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (Or(permissions.IsAdminUser, WriteTokenOnly),)

	def get(self, request, format = None):

		course_id = request.GET.get('course_id')
		date = request.GET.get('date')

		lectures = Lecture.objects.filter(course = course_id, begin__date = date)
		response = []
		for lecture in lectures:
			student_att = StudentsAttendLectures.objects.filter(lecture = lecture)
			att_list = {att.student.student.user.email: att.present for att in student_att}
			att_list['time'] = lecture.begin.time()
			response.append(att_list)

		return Response(response)

