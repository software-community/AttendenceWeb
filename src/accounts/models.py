from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

from django.db import models


def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s_%s.%s" % (instance.student.id, instance.timestamp, ext)
	foldername = "%s" % ("Students_Image")
	return os.path.join(foldername, filename)

class Profile(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	is_student = models.BooleanField(default = False)
	is_teacher = models.BooleanField(default = False)	

	def __str__(self):
		return self.user.username


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
		return self.teacher.user.get_full_name() + '_' + self.teacher.user.email

class StudentImage(models.Model):

	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add = True)
	image = models.ImageField(upload_to=get_file_path)
	

	def is_owner(self, user):
		if self.student.student.user == user:
			return True
		return False
	
	def delete(self, *args, **kwargs):
		print("ddd")
        # You have to prepare what you need before delete the model
		storage, path = self.image.storage, self.image.path
        # Delete the model before the file
		super(StudentImage, self).delete(*args, **kwargs)
        # Delete the file after the model
		storage.delete(path)
	

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


@receiver(models.signals.post_delete, sender=StudentImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=StudentImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)