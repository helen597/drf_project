from rest_framework import serializers
from studying.models import Course, Lesson
from studying.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()
