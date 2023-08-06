from rest_framework.filters import BaseFilterBackend


class GuardianViewPermissionsFilter(BaseFilterBackend):
    """
    A filter backend that limits results to those where they are the foreign key 'user'
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.can_view()