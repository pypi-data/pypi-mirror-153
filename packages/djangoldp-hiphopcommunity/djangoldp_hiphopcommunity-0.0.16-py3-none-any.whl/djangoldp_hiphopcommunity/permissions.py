
from djangoldp.permissions import SuperUserPermission
from djangoldp_hiphopcommunity.filters import *
  

class ProjectmemberPermissions(SuperUserPermission):
    filter_backends = [ProjectmemberFilterBackend]

    def get_object_permissions(self, request, view, obj):

        perms = super().get_object_permissions(request, view, obj)

        # a premium member can change its own project
        if request.user == obj.user:
            perms = perms.union({'view', 'change'})

        return perms

class ToolandCampainPermissions(SuperUserPermission):
    filter_backends = [ToolandCampainFilterBackend]

    def get_container_permissions(self, request, view, obj):
        from .models import Projectmember

        perms = super().get_container_permissions(request, view, obj)

        # a premium member can view all projects
        if Projectmember.objects.filter(user=request.user).exists():
          perms = perms.union({'view'})

        return perms