from rest_framework import permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Verify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


class WriteTokenOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            token = request.META['HTTP_AUTHORIZATION']
            print("Token: ", token)
            decoded_token = auth.verify_id_token(token)
            print(decoded_token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            return True
        except:
            return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            token = request.META['HTTP_AUTHORIZATION']
            print("Token: ", token)
            decoded_token = auth.verify_id_token(token)
            print(decoded_token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            django_user = get_object_or_404(User, email=user.email)
            return obj.is_owner(django_user)
        except:
            return False


