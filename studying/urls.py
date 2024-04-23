from django.urls import path

from studying.apps import StudyingConfig
from rest_framework.routers import DefaultRouter
from studying.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateAPIView, PaymentListAPIView

app_name = StudyingConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons-create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons-get'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lessons-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lessons-delete'),

    path('payment/create', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list')
] + router.urls
