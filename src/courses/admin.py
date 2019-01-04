from django.contrib import admin

from .models import Course, TeachersTeachCourses
# Register your models here.


class CourseAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ["name", "code", "id"]

	search_fields = ["name", "code", "id"]

	class Meta:
		model = Course

admin.site.register(Course, CourseAdminModel)

class TeachersTeachCoursesAdminModel(admin.ModelAdmin):

	list_display = ["teacher", "course", "year", "semester", "id"]

	class Meta:
		model = TeachersTeachCourses

admin.site.register(TeachersTeachCourses, TeachersTeachCoursesAdminModel)

