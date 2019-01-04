from django.contrib import admin

from .models import Lecture, LectureImage, StudentsAttendLectures

# Register your models here.

class LectureAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ["course", "begin", "end", "id"]

	class Meta:
		model = Lecture

admin.site.register(Lecture, LectureAdminModel)

class LectureImageAdminModel(admin.ModelAdmin):

	list_display = ["lecture", "image", "timestamp", "id"]

	class Meta:
		model = LectureImage


admin.site.register(LectureImage, LectureImageAdminModel)

class StudentsAttendLecturesModelAdmin(admin.ModelAdmin):

	list_display = ["lecture", "student", "present", "id"]

	class Meta:
		model = StudentsAttendLectures


admin.site.register(StudentsAttendLectures, StudentsAttendLecturesModelAdmin)


