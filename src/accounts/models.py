from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	is_student = models.BooleanField(default = False)
	is_teacher = models.BooleanField(default = False)	

	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	"""
	Creates a user profile just after a user is created
	"""
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()


class Student(models.Model):
	"""
	Student Model
	"""
	student = models.OneToOneField(Profile, on_delete = models.CASCADE)

	def __str__(self):
		return self.student.user.username


class Teacher(models.Model):
	"""
	Teacher Model
	"""
	teacher = models.OneToOneField(Profile, on_delete = models.CASCADE)

	def __str__(self):
		return self.teacher.user.username

@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
	"""
	Creates a user profile just after a user is created
	"""
	if instance.is_student:
		if not Student.objects.filter(student = instance).exists():
			Student.objects.create(student=instance)
			instance.student.save()

	elif instance.is_teacher:
		if not Teacher.objects.filter(teacher = instance).exists():
			Teacher.objects.create(teacher=instance)
			instance.teacher.save()



