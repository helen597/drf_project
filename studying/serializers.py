from rest_framework import serializers
from studying.models import Course, Lesson, Subscription
from studying.validators import VideoLinkValidator
from users.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_subscription(self, instance):
        user = self.request.user
        return Subscription.objects.all().filter(user=user).filter(course=instance).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
