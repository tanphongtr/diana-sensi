from rest_framework.permissions import BasePermission
from app.models import User

class IsOwnerUser(BasePermission):
    """
    Allows only OWNER role access
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (User.RoleChoices.OWNER in request.user.groups.values_list('name', flat=True))
        )

class IsShipperUser(BasePermission):
    """
    Allows only SHIPPER role access
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (User.RoleChoices.SHIPPER in request.user.groups.values_list('name', flat=True))
        )


class IsCollectorUser(BasePermission):
    """
    Allows only COLLECTOR role access
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (User.RoleChoices.COLLECTOR in request.user.groups.values_list('name', flat=True))
        )