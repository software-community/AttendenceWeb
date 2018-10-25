from django.db import models

from accounts.models import Teacher, Student
from courses.models import Course, TeachersTeachCourses

# Create your models here.

class Lecture(models.Model):

	course = models.ForeignKey(TeachersTeachCourses, on_delete = models.CASCADE)
	begin = models.DateTimeField()
	end = models.DateTimeField()

	student_attendance = models.ManyToManyField(Student, through = 'StudentsAttendLectures')


class StudentsAttendLectures(models.Model):

	lecture = models.ForeignKey(Lecture, on_delete = models.CASCADE)
	student = models.ForeignKey(Student, on_delete = models.CASCADE)

	present = models.BooleanField(default = False)
	# attendance_queries = models.ManyToManyField(LectureImage, through = 'StudentAttendanceQueries')

class LectureImage(models.Model):

	lecture = models.ForeignKey(Lecture, on_delete = models.CASCADE)
	image = models.ImageField()
	timestamp = models.DateTimeField(auto_now_add = True)




