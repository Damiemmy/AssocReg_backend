from django.shortcuts import render
from api import serializers as api_serializer
from core.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from decimal import Decimal
# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=[AllowAny]
    serializer_class=api_serializer.RegisterSerializer

def generate_random_otp(length=7):
    otp=''.join([str(random.randint(0,9)) for _ in range(length)])
    return otp
class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer

    def get_object(self):
        email = self.kwargs.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate token and OTP
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f"{settings.FRONTEND_SITE_URL}create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"

            context = {
                "link": link,
                "username": user.username
            }

            subject = "Password Reset Email"
            context = {
                "link": link,
                "username": user.username
            }
            text_body = render_to_string("email/password_reset.txt", context)
            html_body = render_to_string("email/password_reset.html", context)

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL,  # must match verified SendGrid email
                to=[user.email],
                body=text_body,
                reply_to=[settings.DEFAULT_FROM_EMAIL]   # optional but recommended
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            print("Password reset link:", link)

        return user