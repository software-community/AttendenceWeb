from django.conf import settings
from rest_framework import serializers
from .models import Lecture, LectureImage, StudentsAttendLectures

class LectureSerializer(serializers.ModelSerializer):

	class Meta:
		model = Lecture
		fields = '__all__'


class LectureImageSerializer(serializers.ModelSerializer):

	class Meta:
		model = LectureImage
		fields = '__all__'


class StudentsAttendLecturesSerializer(serializers.ModelSerializer):

	class Meta:
		model = StudentsAttendLectures
		fields = '__all__'