from rest_framework.permissions import BasePermission

class IsMemberOfAdmin(BasePermission):
    """
    Allows access only to users who are members of a admin group.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsMemberOfCoach(BasePermission):
    """
    Allows access only to users who are members of a admin group.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Coach').exists()

class IsMemberOfPlayer(BasePermission):
    """
    Allows access only to users who are members of a admin group.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Player').exists()


class IsMemberOfCoachOrAdmin(BasePermission):
    """
    Allows access only to users who are members of a admin group.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Coach','Admin']).exists()