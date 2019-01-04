from django.db import models

from accounts.models import Teacher, Student
# Create your models here.

class Course(models.Model):

	name = models.CharField(max_length = 120, null = True)
	code = models.CharField(max_length = 6, null = True)

	teachers = models.ManyToManyField(Teacher, through = 'TeachersTeachCourses')

	def __str__(self):
		return self.name

	def is_owner(self, user):
		return user.is_staff



class TeachersTeachCourses(models.Model):

	teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	students = models.ManyToManyField(Student, related_name = 'Students', through = 'StudentAttendCourses')
	teaching_assistants = models.ManyToManyField(Student, related_name = 'TAs', blank = True)

	year = models.IntegerField(null = True)
	semester = models.IntegerField(null = True)
	

	def __str__(self):
		return self.course.name + "-" + str(self.teacher)

	def is_owner(self, user):
		if self.teacher.teacher.user == user:
			return True
		return False


class StudentAttendCourses(models.Model):

	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	course = models.ForeignKey(TeachersTeachCourses, on_delete = models.CASCADE)

	def __str__(self):
		return self.course.course.name + "-" + str(self.student)


