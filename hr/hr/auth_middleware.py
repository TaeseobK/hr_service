from django.contrib.auth import get_user_model
from .local_settings import AUTH_SERVICE
from django.shortcuts import redirect
import requests, jwt, threading
from .thread_locals import *
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .local_settings import BASE_DIR
from pathlib import Path

# Thread-local storage untuk simpan user_id
_thread_locals = threading.local()
PUBLIC_KEY = Path(BASE_DIR, 'keys/public.pem').read_text()

class VerifyAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith(("/api/docs", "/api/schema", "/admin", "/static")):
            return None

        auth_header = request.headers.get("Authorization", "")
        sessionid = request.COOKIES.get("sessionid")

        # fallback parse dari header Cookie kalau gagal
        if not sessionid:
            raw_cookie = request.headers.get("Cookie", "")
            for part in raw_cookie.split(";"):
                if part.strip().startswith("sessionid="):
                    sessionid = part.strip().split("=", 1)[1]

        # Case 1: Frontend request pakai sessionid
        if sessionid:
            try:
                resp = requests.post(
                    f"{AUTH_SERVICE}/api/auth/verify-session/",
                    cookies={"sessionid": sessionid},
                    timeout=10
                )
                if resp.status_code != 200:
                    return JsonResponse({"detail": "Invalid session"}, status=401)

                data = resp.json()
                request.user_id = data.get("user_id")
                request.internal_token = data.get("internal_token")
                set_current_user_id(request.user_id)
                
                return None

            except requests.RequestException:
                return JsonResponse({"detail": "Cannot reach AUTH"}, status=503)

        # Case 2: Service → Service pakai Bearer token
        elif auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            try:
                payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
                request.user_id = payload.get("user_id")
                return None
            except jwt.ExpiredSignatureError:
                return JsonResponse({"detail": "Internal token expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"detail": "Invalid internal token"}, status=401)

        return JsonResponse({"detail": "Missing Authorization or sessionid"}, status=401)

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
                print(data)

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