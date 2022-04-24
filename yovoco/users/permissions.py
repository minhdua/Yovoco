from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError, AccessToken
from rest_framework.exceptions import AuthenticationFailed

from users.models import CustomUser

class IsVerifiedEmail(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_verified_email