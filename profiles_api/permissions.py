from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Membuat permission hanya bisa edit profile sendiri"""
    
    def has_object_permission(self, request, view, obj):
        """Mengecek apakah user berusaha unutk mengedit profile sendiri"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Memperbolehkan user hanya mengupdate feed sendiri"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id