from djangoldp.filters import LDPPermissionsFilterBackend
from rest_framework_guardian.filters import ObjectPermissionsFilter
from djangoldp.utils import is_anonymous_user

class ProjectmemberFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        from .models import Projectmember
        if is_anonymous_user(request.user):
            return view.model.objects.none()
        elif request.user.is_superuser:
            return queryset
        elif Projectmember.objects.filter(user=request.user).exists():
            return queryset.filter(user=request.user)
        else:
            return view.model.objects.none()

class ToolandCampainFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        from .models import Projectmember
        if is_anonymous_user(request.user):
            return view.model.objects.none()
        elif request.user.is_superuser:
            return queryset
        elif Projectmember.objects.filter(user=request.user).exists():
            return queryset
        else:
            return view.model.objects.none()