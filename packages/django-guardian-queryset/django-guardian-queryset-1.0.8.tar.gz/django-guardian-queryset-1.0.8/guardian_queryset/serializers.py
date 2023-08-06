import types

from django.db.models import QuerySet, Manager
from rest_framework import serializers
from rest_framework.relations import RelatedField

from guardian_queryset.utils import has_view_permissions
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin


def get_queryset_guardian(self):
    queryset = self.queryset
    if isinstance(queryset, (QuerySet, Manager)):
        queryset = queryset.all()
        try:
            queryset = queryset.can_view()
        except:
            pass
        # if hasattr(queryset, "can_view"):
    return queryset


def run_validator_with_class(cls):
    def run_validators(self, value):
        for validator in self.validators:
            try:
                validator.queryset = validator.queryset.can_view()
            except:
                pass
        return super(cls, self).run_validators(value)
    return run_validators


class ValidateForeignKeyUserMixin(serializers.Serializer):

    @property
    def _writable_fields(self):
        for field in self.fields.values():
            if not field.read_only:
                # if isinstance(field, RelatedField) or issubclass(type(field), RelatedField):
                if isinstance(field, RelatedField):
                    field.get_queryset = types.MethodType(get_queryset_guardian, field)
                    field.run_validators = types.MethodType(run_validator_with_class(type(field)), field)
                yield field

    @property
    def _readable_fields(self):
        for field in self.fields.values():
            if not field.write_only:
                if isinstance(field, RelatedField):
                    field.get_queryset = types.MethodType(get_queryset_guardian, field)
                    field.run_validators = types.MethodType(run_validator_with_class(type(field)), field)
                yield field

    def get_unchecked_foreignkey_fields(self):
        return []

    def get_user_field_name(self):
        return 'user'

    # TODO: fix user check
    def validate(self, data):
        current_user = self.context['request'].user
        for name, field in self.get_fields().items():
            if isinstance(field, RelatedField) or issubclass(type(field), RelatedField):
            # if type(field) == PrimaryKeyRelatedField:
                if name not in self.get_unchecked_foreignkey_fields():
                    if not field.read_only:
                        if name == self.get_user_field_name():
                            if data[self.get_user_field_name()] != current_user:
                                raise serializers.ValidationError("attempted to create foreign key on unauthorized object")
                        elif name in data and not has_view_permissions(current_user, data):
                            raise serializers.ValidationError("attempted to create foreign key on unauthorized object")
        return data

class AssignActiveUserDefaultPermissionMixin(ObjectPermissionsAssignmentMixin):

    def get_permissions_map(self, created):
        current_user = self.context['request'].user
        model_name = self.Meta.model.__name__.lower()

        return {
            'view_' + model_name: [current_user],
            'change_' + model_name: [current_user],
            'delete_' + model_name: [current_user]
        }

