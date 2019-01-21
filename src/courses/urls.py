from django.urls import path, include
from . import views
from .api import CourseViewSet, TeachersTeachCoursesViewSet, StudentAttendance

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('course', CourseViewSet)
router.register('ttc', TeachersTeachCoursesViewSet)


urlpatterns = [
	path('api/', include(router.urls)),
	path('add-courses/', views.add_courses),
	path('get-attendance/', StudentAttendance.as_view())
]