from django.db import models

from accounts.models import Teacher, Student
# Create your models here.

class Course(models.Model):

	name = models.CharField(max_length = 120, null = True)
	code = models.CharField(max_length = 6, null = True)

	teachers = models.ManyToManyField(Teacher, through = 'TeachersTeachCourses')

	def __str__(self):
		return self.name


class TeachersTeachCourses(models.Model):

	teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	students = models.ManyToManyField(Student, related_name = 'Students')
	teaching_assistants = models.ManyToManyField(Student, related_name = 'TAs')

	year = models.IntegerField(null = True)
	semester = models.IntegerField(null = True)
	

	def __str__(self):
		return self.course.name + "-" + str(self.teacher)


