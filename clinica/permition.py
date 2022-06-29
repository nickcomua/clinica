from rest_framework import permissions
from .models import *
class AppointmentPer(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """ 
    def has_permission(self, request, view):
        print(request.method)
        if (request.method in permissions.SAFE_METHODS):
            return True
        if (request.data == {}):
            return True
        print(request.user.id)
        print(request.data)
        try:
            if (Client.objects.get(user_id=request.user.id).id == request.data['client']):
                return True
            if (Worker.objects.get(user_id=request.user.id).id == request.data['worker']):
                return True
        except:
            None
        print('has_permission')
        if (request.user.is_superuser):
            return True 
        return False
    def has_object_permission(self, request, view, obj):
        if (request.user.is_superuser):
            return True 
        return ((obj.client.user_id == request.user.id) | (obj.worker.user_id == request.user.id))