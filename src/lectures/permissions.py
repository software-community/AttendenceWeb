from rest_framework import permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class TokenVerified(permissions.BasePermission):
    """
    Verifies the Token
    """

    def has_permission(self, request, view):

        if request.method == 'POST':
            try:
                token = request.POST.get('id_token')
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
                return True
            except:
                return False

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
            token = request.POST.get('id_token')
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            django_user = get_object_or_404(User, email=user.email)
            print(Here)
            return obj.is_owner(django_user)
        except:
            return False