from django_utils.views import as_response
from guardian_queryset.filters import GuardianViewPermissionsFilter



def as_protected_response(
        *args,
        **kwargs
):
    if not "filter_backends" in kwargs:
        kwargs["filter_backends"] = []
    kwargs["filter_backends"].append(GuardianViewPermissionsFilter)
    return as_response(*args, **kwargs)