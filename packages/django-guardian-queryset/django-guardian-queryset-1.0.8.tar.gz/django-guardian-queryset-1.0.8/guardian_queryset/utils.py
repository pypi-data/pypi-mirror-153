from django.conf import settings
from django.db.models import ForeignKey
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework.exceptions import ValidationError

PUBLIC_VIEW_MODELS_LOWER = [model_name.lower() for model_name in getattr(settings, 'PUBLIC_VIEW_MODELS', [])]

def get_model_name(obj_or_query):
    try:
        return obj_or_query.model.__name__.lower()
    except Exception:
        return obj_or_query._meta.model.__name__.lower()

def assign_default_permissions(user, object, model_name=None):
    model_name = model_name or get_model_name(object)
    assign_perm('view_' + model_name, user, object)
    assign_perm('change_' + model_name, user, object)
    assign_perm('delete_' + model_name, user, object)


def assign_view_permissions(user, object, save=True):
    model_name = get_model_name(object)
    assign_perm('view_' + model_name, user, object)


def assign_change_permissions(user, object, save=True):
    model_name = get_model_name(object)
    assign_perm('change_' + model_name, user, object)


def remove_view_permissions(user, object):
    model_name = get_model_name(object)
    remove_perm('view_' + model_name, user, object)


def has_permissions(user, object, permission):
    model_name = get_model_name(object)
    return user.has_perm(permission + model_name, object)


def has_view_permissions(user, object):
    model_name = get_model_name(object)
    return model_name in PUBLIC_VIEW_MODELS_LOWER or has_permissions(user, object, 'view_')

def has_change_permissions(user, object):
    return has_permissions(user, object, 'change_')

def has_delete_permissions(user, object):
    return has_permissions(user, object, 'delete_')


def validate_foreign_keys(user, object, user_field_name="user", unchecked_field_names=[]):
    for attr_name in dir(object._meta.model):
        attr = getattr(object._meta.model, attr_name)
        if hasattr(attr, 'field'):
            field = attr.field
            if isinstance(attr.field, ForeignKey):
                if hasattr(object, field.name) and field.name not in unchecked_field_names:
                    related_object = getattr(object, field.name)
                    if related_object:
                        from guardian_queryset.models import GuardianModel
                        if field.name == user_field_name:
                            if related_object != user:
                                raise ValidationError(f"attempted to create foreign key on unauthorized object {related_object}")
                        elif isinstance(related_object, GuardianModel) and not has_view_permissions(user, related_object):
                            raise ValidationError(f"attempted to create foreign key on unauthorized object {related_object}")