from django.urls import path, include
from . import views
from .api import CourseViewSet, TeachersTeachCoursesViewSet, StudentAttendance, TotalStudentAttendance

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('course', CourseViewSet)
router.register('ttc', TeachersTeachCoursesViewSet)


urlpatterns = [
	path('api/', include(router.urls)),
	path('add-courses/', views.add_courses),
	path('get-attendance/', StudentAttendance.as_view()),
	path('get-total-attendance/', TotalStudentAttendance.as_view()),
	path('register-course/', views.add_student),
	path('add-ta/', views.add_ta)
]