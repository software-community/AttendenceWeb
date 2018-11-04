from django.urls import path, include
from . import views
from .api import LectureViewSet, LectureImageViewSet, StudentsAttendLecturesViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('lecture', LectureViewSet)
router.register('lecture-image', LectureImageViewSet)
router.register('sal', StudentsAttendLecturesViewSet)


urlpatterns = [
	path('api/', include(router.urls)),
]