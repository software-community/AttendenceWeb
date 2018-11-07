from django.db import models

from accounts.models import Teacher, Student
from courses.models import Course, TeachersTeachCourses
import os,uuid

# Create your models here.

def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s_%s.%s" % (instance.lecture.begin,instance.lecture.end, ext)
	foldername = "%s_%s" % (instance.lecture.course,instance.lecture.course.teacher)
	return os.path.join(foldername, filename)

class Lecture(models.Model):

	course = models.ForeignKey(TeachersTeachCourses, on_delete = models.CASCADE)

	begin = models.DateTimeField()
	end = models.DateTimeField()

	student_attendance = models.ManyToManyField(Student, through = 'StudentsAttendLectures')

	def __str__(self):
		return str(self.course) + "-" + str(self.id)
		
	def save(self, *args, **kwargs):
		if not self.begin:
			self.begin = None
		if not self.end:
			self.end = None
		super(Lecture, self).save(*args, **kwargs)


class StudentsAttendLectures(models.Model):

	lecture = models.ForeignKey(Lecture, on_delete = models.CASCADE)
	student = models.ForeignKey(Student, on_delete = models.CASCADE)

	present = models.BooleanField(default = False)
	# attendance_queries = models.ManyToManyField(LectureImage, through = 'StudentAttendanceQueries')


	#def __str__(self):
	#	return str(lecture) + "-" + str(student)

	def is_owner(self, user):
		if self.lecture__course__teacher__teacher__user == user:
			return True
		return False


class LectureImage(models.Model):

	lecture = models.ForeignKey(Lecture, on_delete = models.CASCADE)
	image = models.ImageField(upload_to=get_file_path)
	timestamp = models.DateTimeField(auto_now_add = True)


	#def __str__(self):
	#	return str(lecture) + str(timestamp)

