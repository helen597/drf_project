from rest_framework import serializers

from studying.serializers import LessonSerializer, CourseSerializer
from users.models import User, Payment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from studying.serializers import CourseSerializer, LessonSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен

        token['email'] = user.email

        return token
