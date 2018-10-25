from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	is_student = models.BooleanField(default = False)
	is_teacher = models.BooleanField(default = False)	


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


class Teacher(models.Model):
	"""
	Teacher Model
	"""
	teacher = models.OneToOneField(Profile, on_delete = models.CASCADE)