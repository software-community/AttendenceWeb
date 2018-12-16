from django.urls import path, include
from . import views
from .api import LectureViewSet, LectureImageViewSet, StudentsAttendLecturesViewSet, StudentLectures

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('lecture', LectureViewSet)
router.register('lecture-image', LectureImageViewSet)
router.register('sal', StudentsAttendLecturesViewSet)
router.register('student-lectures', StudentLectures)



urlpatterns = [
	path('api/', include(router.urls)),
]