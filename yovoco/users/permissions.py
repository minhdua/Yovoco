from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions

from users.models import CustomUser

class IsVerifiedEmail(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_verified_email
    
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        print('obj,',obj)
        return obj.created_by == request.user
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
    
class IsNotDeleted(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_deleted == False
    
