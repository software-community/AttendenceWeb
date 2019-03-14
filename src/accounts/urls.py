from django.urls import path, include
from . import views
from .api import ProfileViewSet, StudentViewSet, TeacherViewSet, StudentImageViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', ProfileViewSet)
router.register('student', StudentViewSet)
router.register('teacher', TeacherViewSet)
router.register('student-image', StudentImageViewSet)


urlpatterns = [
	path('api/', include(router.urls)),
	path('token-auth/', views.tokenAuth),
	path('token-login/', views.login)
]