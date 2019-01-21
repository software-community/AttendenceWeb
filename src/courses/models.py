from django.db import models

from accounts.models import Teacher, Student
from django.utils.crypto import get_random_string
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
	teaching_assistants = models.ManyToManyField(Teacher, related_name = 'TAs', blank = True)

	year = models.IntegerField(null = True)
	semester = models.IntegerField(null = True)

	student_code = models.CharField(max_length = 5, unique = True, blank = True, null = True)
	ta_code = models.CharField(max_length = 5, unique = True, blank = True, null = True)
	

	def __str__(self):
		return self.course.name + "-" + str(self.teacher)

	def is_owner(self, user):
		if self.teacher.teacher.user == user:
			return True
		return False

	def _unique_student_code(self):

		code = get_random_string(length = 5)
		while TeachersTeachCourses.objects.filter(student_code = code).exists():
			code = get_random_string(length = 5)
		return code

	def _unique_ta_code(self):

		code = get_random_string(length = 5)
		while TeachersTeachCourses.objects.filter(ta_code = code).exists():
			code = get_random_string(length = 5)
		return code

	def save(self, *args, **kwargs):
		if not self.student_code:
			self.student_code = self._unique_student_code()
		if not self.teacher_code:
			self.ta_code = self._unique_ta_code()

		super().save(*args, **kwargs)


class StudentAttendCourses(models.Model):

	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	course = models.ForeignKey(TeachersTeachCourses, on_delete = models.CASCADE)

	def __str__(self):
		return self.course.course.name + "-" + str(self.student)


