from django.db import models

from global_requests import get_thread_user
from guardian_queryset.manager import GuardianManager
from guardian_queryset.queryset import InvalidOperation
from guardian_queryset.utils import assign_default_permissions, has_change_permissions, has_delete_permissions
from django_utils.utils import is_anonymous_user


class GuardianModel(models.Model):

    # __default_manager = _InternalGuardianManager()
    objects = GuardianManager()
    _objects = models.Manager()

    # @classmethod
    # def objects(cls, user):
    #     return cls._guardian_objects.with_user(user)

    class Meta:
        abstract = True

    def get_user(self, user, use_obj_user):
        user = user or get_thread_user()
        if use_obj_user and is_anonymous_user(user):
            try:
                user = self.user
            except:
                raise AssertionError("Model doesn't have a user")
        assert not user.is_anonymous, "User for saving is anonymous"
        return user

    def _save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def save(self, *args, user=None, use_obj_user=True, **kwargs):
        user = self.get_user(user, use_obj_user)
        if self._state.adding or not self.pk:
            super().save(*args, **kwargs)
            assign_default_permissions(user, self)
            return super().save()
        else:
            if not has_change_permissions(user, self):
                raise InvalidOperation("User does not have permission to update this object")
            return super().save(*args, **kwargs)


    def _delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def delete(self, *args, user=None, use_obj_user=True, **kwargs):
        user = self.get_user(user, use_obj_user)
        if not has_delete_permissions(user, self):
            raise InvalidOperation("User does not have permission to delete this object")
        return super().delete(*args, **kwargs)

    # def _perform_unique_checks(self, unique_checks):
    #     errors = {}
    #
    #     for model_class, unique_check in unique_checks:
    #         # Try to look up an existing object with the same values as this
    #         # object's values for all the unique field.
    #
    #         lookup_kwargs = {}
    #         for field_name in unique_check:
    #             f = self._meta.get_field(field_name)
    #             lookup_value = getattr(self, f.attname)
    #             # TODO: Handle multiple backends with different feature flags.
    #             if (lookup_value is None or
    #                     (lookup_value == '' and connection.features.interprets_empty_strings_as_nulls)):
    #                 # no value, skip the lookup
    #                 continue
    #             if f.primary_key and not self._state.adding:
    #                 # no need to check for unique primary key when editing
    #                 continue
    #             lookup_kwargs[str(field_name)] = lookup_value
    #
    #         # some fields were skipped, no reason to do the check
    #         if len(unique_check) != len(lookup_kwargs):
    #             continue
    #
    #
    #         qs = model_class._default_manager.filter(**lookup_kwargs)
    #         try:
    #             qs = qs.force_validate()
    #         except Exception:
    #             pass
    #
    #         # Exclude the current object from the query if we are editing an
    #         # instance (as opposed to creating a new one)
    #         # Note that we need to use the pk as defined by model_class, not
    #         # self.pk. These can be different fields because model inheritance
    #         # allows single model to have effectively multiple primary keys.
    #         # Refs #17615.
    #         model_class_pk = self._get_pk_val(model_class._meta)
    #         if not self._state.adding and model_class_pk is not None:
    #             qs = qs.exclude(pk=model_class_pk)
    #         if qs.exists():
    #             if len(unique_check) == 1:
    #                 key = unique_check[0]
    #             else:
    #                 key = NON_FIELD_ERRORS
    #             errors.setdefault(key, []).append(self.unique_error_message(model_class, unique_check))
    #
    #     return errors
    #
    # def clean_fields(self, exclude=None):
    #     """
    #     Clean all fields and raise a ValidationError containing a dict
    #     of all validation errors if any occur.
    #     """
    #     if exclude is None:
    #         exclude = []
    #
    #     errors = {}
    #     for f in self._meta.fields:
    #         if f.name in exclude:
    #             continue
    #         # Skip validation for empty fields with blank=True. The developer
    #         # is responsible for making sure they have a valid value.
    #         raw_value = getattr(self, f.attname)
    #         if f.blank and raw_value in f.empty_values:
    #             continue
    #         try:
    #             if isinstance(f, ForeignKey):
    #             setattr(self, f.attname, f.clean(raw_value, self))
    #         except ValidationError as e:
    #             errors[f.name] = e.error_list
    #
    #     if errors:
    #         raise ValidationError(errors)