from django.db import models

from accounts.models import Teacher, Student
from courses.models import Course, TeachersTeachCourses

# Create your models here.

class Lecture(models.Model):

	course = models.ForeignKey(TeachersTeachCourses, on_delete = models.CASCADE)
	begin = models.DateTimeField(null = True,blank=True)
	end = models.DateTimeField(null = True,blank=True)

	student_attendance = models.ManyToManyField(Student, through = 'StudentsAttendLectures')

	#def __str__(self):
	#	return str(self.course) + str(begin) + "-" + str(end)
		
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

class LectureImage(models.Model):

	lecture = models.ForeignKey(Lecture, on_delete = models.CASCADE)
	image = models.ImageField()
	timestamp = models.DateTimeField(auto_now_add = True)

	#def __str__(self):
	#	return str(lecture) + str(timestamp)




