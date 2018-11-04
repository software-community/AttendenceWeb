from django.urls import path, include
from . import views
from .api import CourseViewSet, TeachersTeachCoursesViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('course', CourseViewSet)
router.register('ttc', TeachersTeachCoursesViewSet)


urlpatterns = [
	path('api/', include(router.urls)),
]