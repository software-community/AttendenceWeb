from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import BaseFilterBackend
from django.shortcuts import render, get_object_or_404, redirect
from lectures.models import Lecture

# Verify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import datetime

class GetCurrentLectures(BaseFilterBackend):
	"""
	Gets today lectures for the student
	"""
	def filter_queryset(self, request, queryset, view):
		print(datetime.datetime.now().date())
		today = datetime.datetime.now().date()
		try:
			token = request.META['HTTP_AUTHORIZATION']
			print("Token: ", token)
			decoded_token = auth.verify_id_token(token)
			print(decoded_token)
			uid = decoded_token['uid']
			user = auth.get_user(uid)
			django_user = get_object_or_404(User, email=uid.email)
			lectures = Lecture.objects.all().filter(begin__date = today)
			return queryset.filter(student = django_user.profile.student, lecture__in = lectures)
		except:
			return None
