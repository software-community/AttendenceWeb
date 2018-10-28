from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from .models import Course, TeachersTeachCourses

from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.filters import SearchFilter


from .serializers import CourseSerializer, TeachersTeachCoursesSerializer


class CourseViewSet(viewsets.ModelViewSet):
	
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('name', 'teachers', 'students', 'teaching_assistants', )

class TeachersTeachCoursesViewSet(viewsets.ModelViewSet):
	
	queryset = TeachersTeachCourses.objects.all()
	serializer_class = TeachersTeachCoursesSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('teacher', 'course',)
	search_fields = ('teacher__user__first_name', 'teacher__user__last_name')
