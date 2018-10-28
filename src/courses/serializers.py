from django.conf import settings
from rest_framework import serializers
from .models import Course, TeachersTeachCourses

class CourseSerializer(serializers.ModelSerializer):

	class Meta:
		model = Course
		fields = '__all__'


class TeachersTeachCoursesSerializer(serializers.ModelSerializer):

	class Meta:
		model = TeachersTeachCourses
		fields = '__all__'