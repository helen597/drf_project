from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from users.serializers import MyTokenObtainPairSerializer, UserSerializer
import secrets
import string
import pytz
from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from config import settings
from users.models import User


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def perform_authentication(self, request):
        user = User.objects.filter(verification_code=self.request.token).first()
        if user:
            zone = pytz.timezone(settings.TIME_ZONE)
            user.last_login = datetime.now(zone)
            user.save()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


def verification_view(request, token):
    user = User.objects.filter(verification_code=token).first()
    if user:
        user.is_active = True
        user.save()
    return redirect('users:login')


def recover_password(request):
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(10))
    request.user.set_password(password)
    request.user.save()
    message = f"Ваш новый пароль:\n{password}"
    send_mail(
        "Смена пароля",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )
    return redirect(reverse('catalog:product_list'))
