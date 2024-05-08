import requests
from rest_framework import viewsets, generics, serializers
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from studying.paginators import MyPagination
from users.permissions import IsModer, IsOwner
from users.models import Payment
from studying.models import Course, Lesson, Subscription
from studying.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer, PaymentSerializer
from rest_framework import status
from studying.services import create_product, create_price, create_session


class CourseViewSet(viewsets.ModelViewSet):
    """Viewset for courses"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ["retrieve", "update"]:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModer, IsOwner]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModer]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """Lesson create endpoint"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Lesson list endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def get(self, request, *args, **kwargs):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Lesson retrieve endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Lesson update endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Lesson delete endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Payment create endpoint"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            payment = serializer.save(user=self.request.user)
            product = payment.paid_lesson if payment.paid_lesson else payment.paid_course
            stripe_product = create_product(product)
            price = create_price(product.price, stripe_product)
            session_id, payment_link = create_session(price)
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
        except serializers.ValidationError("Выберите урок или курс для оплаты") as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentListAPIView(generics.ListAPIView):
    """Payment list endpoint"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'method',)
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]


class SubscriptionAPIView(APIView):
    """Lesson update endpoint"""
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(course=course).first()

        if subs_item:
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            new_sub = Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})
