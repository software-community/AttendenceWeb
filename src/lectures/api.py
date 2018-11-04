from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from .models import Lecture, LectureImage, StudentsAttendLectures

from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.filters import SearchFilter


from .serializers import LectureImageSerializer, LectureSerializer, StudentsAttendLecturesSerializer


class LectureViewSet(viewsets.ModelViewSet):
	
	queryset = Lecture.objects.all()
	serializer_class = LectureSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('course',)

class StudentsAttendLecturesViewSet(viewsets.ModelViewSet):
	
	queryset = StudentsAttendLectures.objects.all()
	serializer_class = StudentsAttendLecturesSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('lecture', 'student',)

class LectureImageViewSet(viewsets.ModelViewSet):
	
	queryset = LectureImage.objects.all()
	serializer_class = LectureImageSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('lecture', )