from rest_framework import permissions

'''
    Custom permission class for only GET method
'''
class IsGetOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        # allow GET request only
        if request.method == 'GET':
            return True

        return request.user and request.user.is_authenticated