from django.urls import path, include
from . import views
from .api import ProfileViewSet, StudentViewSet, TeacherViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', ProfileViewSet)
router.register('student', StudentViewSet)
router.register('teacher', TeacherViewSet)


urlpatterns = [
	path('api/', include(router.urls)),
]