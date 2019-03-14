from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from .models import Profile, Student, Teacher, StudentImage

from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.filters import SearchFilter


from .serializers import ProfileSerializer, StudentSerializer, TeacherSerializer, StudentImageSerializer
from lectures.api import LectureViewSet

from rest_condition import Or
from lectures.permissions import WriteTokenOnly


class ProfileViewSet(viewsets.ModelViewSet):
	
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (Or(permissions.IsAdminUser, WriteTokenOnly),)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('user', 'is_teacher', 'is_student',)
	search_fields = ('user__first_name', 'user__last_name')

class StudentViewSet(viewsets.ModelViewSet):
	
	queryset = Student.objects.all()
	serializer_class = StudentSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (Or(permissions.IsAdminUser, WriteTokenOnly),)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('student',)
	search_fields = ('student__user__first_name',)



class TeacherViewSet(viewsets.ModelViewSet):
	
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (Or(permissions.IsAdminUser, WriteTokenOnly),)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('teacher',)
	search_fields = ('teacher__user__first_name',)


class StudentImageViewSet(viewsets.ModelViewSet):
	
	queryset = StudentImage.objects.all()
	serializer_class = StudentImageSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	#permission_classes = (Or(permissions.IsAdminUser, WriteTokenOnly),)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('student', )
