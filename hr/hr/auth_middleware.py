from django.contrib.auth import get_user_model
from .local_settings import AUTH_SERVICE
from django.shortcuts import redirect
import threading
import requests
from django.http import JsonResponse

# Thread-local storage untuk simpan user_id
_thread_locals = threading.local()

class VerifyAuthTokenMiddleware:
    """
    Middleware global untuk:
    - Verifikasi token dari AUTH_SERVICE
    - Simpan user_id di threadlocal
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default: user belum login
        _thread_locals.user_id = None

        # Lewatkan path yang nggak butuh autentikasi
        if request.path.startswith(("/api/docs/", "/api/schema/", "/admin/")):
            return self.get_response(request)

        # Ambil token dari header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Token "):
            return JsonResponse({'detail': 'Token mana token?'}, status=401)

        token = auth_header.split(" ", 1)[1]

        # Verifikasi token ke AUTH_SERVICE
        try:
            resp = requests.post(
                f"{AUTH_SERVICE}/api/auth/verify-token/",
                headers={"Authorization": f"Token {token}"},
                timeout=5
            )
            if resp.status_code != 200:
                return JsonResponse({"detail": "Invalid token"}, status=401)

            data = resp.json()
            _thread_locals.user_id = data.get("user_id")
        except requests.RequestException:
            return JsonResponse({"detail": "Cannot reach AUTH_SERVICE"}, status=503)

        return self.get_response(request)

User = get_user_model()

class AuthServiceBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            # Hit AUTH_SERVICE login
            login_res = requests.post(
                f"{AUTH_SERVICE}/api/auth/login/",
                data={"username": username, "password": password},
                timeout=5
            )

            if login_res.status_code == 200:
                data = login_res.json()

                # Simpan token & cookies di session Django
                request.session["auth_token"] = data.get("token")
                request.session["auth_cookies"] = data.get("auth_session_id")

                user_data = data.get('user_data', {})
                username = user_data.get('username')
                is_superuser = user_data.get('is_superuser')

                # Kalau superuser, buat user lokal
                if is_superuser:
                    user, _ = User.objects.get_or_create(username=username)
                    user.is_superuser = True
                    user.is_staff = True
                    user.set_password(password)  # biar bisa masuk admin
                    user.save()
                    return user
            return None

        except Exception as e:
            print("Error auth:", e)
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
class AuthServiceLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Cek kalau URL mengarah ke logout admin
        if request.path == "/admin/logout/" and request.method == "POST":
            token = request.session.get("auth_token")
            cookies = request.session.get("auth_cookies")

            if token:
                try:
                    requests.post(
                        f"{AUTH_SERVICE}/api/auth/logout/",
                        headers={
                            'Authorization': f"Token {token}",
                            'Cookie': f"sessionid={cookies}"
                        },
                        timeout=5
                    )
                except Exception as e:
                    print("Logout AUTH_SERVICE gagal:", e)

            # Bersihkan session
            request.session.flush()

            return redirect("/admin/login/")

        return self.get_response(request)