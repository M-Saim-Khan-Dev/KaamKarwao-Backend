from rest_framework.authentication import BaseAuthentication
from types import SimpleNamespace

class GatewayHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.META.get("HTTP_X_USER_ID")
        if not user_id:
            return None

        is_verified = request.META.get("HTTP_X_IS_VERIFIED") == "true"
        is_staff = request.META.get("HTTP_X_IS_STAFF") == "true"

        user = SimpleNamespace(
            id=int(user_id),
            pk=int(user_id),
            is_authenticated=True,
            is_verified=is_verified,
            is_staff=is_staff,
            is_active=True,
        )
        return (user, None)