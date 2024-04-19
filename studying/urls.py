from studying.apps import StudyingConfig
from rest_framework.routers import DefaultRouter
from studying.views import CourseViewSet

app_name = StudyingConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [

] + router.urls
