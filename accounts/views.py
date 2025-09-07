import json
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def google_login(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    token = request.POST.get("credential")
    if not token:
        return JsonResponse({'error': 'No se recibió token'}, status=400)

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            "412755564966-676n6n8qeehofgo4ihmineteauom13e2.apps.googleusercontent.com"
        )
        email = idinfo.get('email')
        nombre = idinfo.get('name', '')

        # Solo usuarios existentes
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no autorizado'}, status=403)

        login(request, user)
        redirect_url = reverse('dashboard_admin') if user.is_staff else reverse('dashboard_user')
        return JsonResponse({'redirect_url': redirect_url})

    except ValueError:
        return JsonResponse({'error': 'Token inválido'}, status=400)
