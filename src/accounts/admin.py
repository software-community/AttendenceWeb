from django.contrib import admin
from .models import Profile, Student, Teacher
# Register your models here.

class ProfileAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ["user", "id"]

	search_fields = ["user", "user.email"]

	class Meta:
		model = Profile

admin.site.register(Profile, ProfileAdminModel)

class StudentAdminModel(admin.ModelAdmin):

	list_display = ["student", "id"]

	class Meta:
		model = Student

admin.site.register(Student, StudentAdminModel)


class TeacherAdminModel(admin.ModelAdmin):

	list_display = ["teacher", "id"]

	class Meta:
		model = Teacher

admin.site.register(Teacher, TeacherAdminModel)