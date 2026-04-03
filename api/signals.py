from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
import requests

@receiver(user_logged_in)
def send_login_email(sender, request, user, **kwargs):
    try:
        requests.post(
            "http://localhost:5678/webhook/user-login",
            json={
                "email": user.email,
                "full_name": user.full_name,
                "reg_number": user.reg_number,
            },
            timeout=5
        )
    except Exception as e:
        # Never break login if n8n is down
        print("n8n login webhook failed:", e)
