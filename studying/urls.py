from django.urls import path

from studying.apps import StudyingConfig
from rest_framework.routers import DefaultRouter
from studying.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView

app_name = StudyingConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons-create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons-get'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lessons-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lessons-delete'),
] + router.urls
