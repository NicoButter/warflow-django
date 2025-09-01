import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from django.contrib.auth import get_user_model
import requests

User = get_user_model()
CLIENT_ID = "356408280239-7airslbg59lt2nped9l4dtqm2rf25aii.apps.googleusercontent.com"

@csrf_exempt 
def google_login(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        token = data.get("id_token")
    except Exception:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)

    # Validar token con Google
    r = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": token})
    if r.status_code != 200:
        return JsonResponse({"success": False, "error": "Token inválido"}, status=400)

    info = r.json()
    email = info.get("email")
    name = info.get("name")

    if not email:
        return JsonResponse({"success": False, "error": "No se pudo obtener el email"}, status=400)

    user, created = User.objects.get_or_create(username=email, defaults={"first_name": name, "email": email})
    login(request, user)  

    return JsonResponse({"success": True})
