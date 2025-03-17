import os
import django

# Configura Django para acceder a settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_snippets.settings")  # Reemplaza "tu_proyecto" con el nombre real de tu proyecto
django.setup()

from django.core.mail import send_mail
from django.conf import settings

try:
    send_mail(
        "Prueba de correo desde Django",
        "Este es un correo de prueba enviado desde Django.",
        settings.EMAIL_HOST_USER,
        ["louidorlove@gmail.com"],  # Cambia por el correo al que quieres enviar la prueba
        fail_silently=False,
    )
    print("✅ ¡Correo enviado correctamente!")
except Exception as e:
    print(f"❌ Error al enviar el correo: {e}")
