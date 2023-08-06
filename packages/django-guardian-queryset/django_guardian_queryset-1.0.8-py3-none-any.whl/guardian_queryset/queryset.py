from functools import reduce

from django.db.models import QuerySet
from global_requests import get_thread_user
from guardian.shortcuts import get_objects_for_user
from guardian_queryset.utils import validate_foreign_keys, assign_default_permissions, PUBLIC_VIEW_MODELS_LOWER
from rest_framework.exceptions import ValidationError


class InvalidOperation(Exception):
    pass


class GuardianQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        self._reset_validation()
        super().__init__(*args, **kwargs)

    def some_oper_validated(self):
        return reduce(lambda x, value:x or value, self._validated_opers.values(), False)


    def __len__(self):
        if self.some_oper_validated():
            return super().__len__()
        else:
            raise InvalidOperation("No operations have been validated")

    def __iter__(self):
        if not self._validated_opers["view"]:
            return self.can_view().__iter__()
            # raise InvalidOperation("View operations have not been validated")
        return super().__iter__()


    @property
    def model_name(self):
        return self.model.__name__.lower()

    @property
    def user(self):
        return get_thread_user()

    def select_for_update(self, *args, **kwargs):
        obj = super().select_for_update(*args, **kwargs)
        obj.can_change()
        obj.force_validate_oper("view")
        return obj

    def create(self, with_user=True, **kwargs):
        if with_user:
            obj = super().create(**{
                'user': self.user,
                **kwargs,
            })
        else:
            obj = super().create(**kwargs)
        try:
            validate_foreign_keys(self.user, obj)
        except ValidationError as e:
            obj.delete()
            raise e
        assign_default_permissions(self.user, obj)
        return obj


    def _reset_validation(self):
        self._validated_opers = {
            "view": False,
            "change": False,
            "delete": False

        }

    def _clone(self):
        c = super()._clone()
        c._validated_opers = self._validated_opers
        return c


    def can_do(self, perms, user=None):
        user = user or self.user
        if len(perms) == 1 and perms[0] == "view" and self.model_name in PUBLIC_VIEW_MODELS_LOWER:
            self._validated_opers["view"] = True
            return self
        else:
            clone = get_objects_for_user(user, [perm + "_" + self.model_name for perm in perms], klass=self)
            for perm in perms:
                if perm == "view":
                   clone._validated_opers["view"] = True
                elif perm == "change":
                    clone._validated_opers["change"] = True
                elif perm == "delete":
                    clone._validated_opers["delete"] = True
            return clone

    def can_view(self, user=None):
        return self.can_do(["view"], user=user)

    def can_change(self, user=None):
        return self.can_do(["change"], user=user)

    def can_delete(self, user=None):
        return self.can_do(["delete"], user=user)

    def is_owner(self, user=None):
        return self.can_do(["view", "change", "delete"], user=user)

    def force_validate(self):
        for oper in self._validated_opers.keys():
            self._validated_opers[oper] = True
        return self

    def force_validate_oper(self, oper):
        if oper in self._validated_opers.keys():
            self._validated_opers[oper] = True
        return self


    def values(self, *args, **kwargs):
        if not self._validated_opers["view"]:
            raise InvalidOperation("View operations have not been validated")
        return super().values(*args, **kwargs)

    def _values_list(self, *args, **kwargs):
        return super().values_list(*args, **kwargs)
    def values_list(self, *args, **kwargs):
        if not self._validated_opers["view"]:
            raise InvalidOperation("View operations have not been validated")
        return super().values_list(*args, **kwargs)

    def _get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
    def get(self, *args, **kwargs):
        if not self._validated_opers["view"]:
            raise InvalidOperation("View operations have not been validated")
        return super().get(*args, **kwargs)

    def _first(self):
        return super().first()
    def first(self):
        if not self._validated_opers["view"]:
            raise InvalidOperation("View operations have not been validated")
        return super().first()

    def _update(self, **kwargs):
        return super().update(**kwargs)
    def update(self, **kwargs):
        if not self._validated_opers["change"]:
            raise InvalidOperation("Update operations have not been validated")
        return super().update(**kwargs)

    def _delete(self):
        return super().delete()
    def delete(self):
        if not self._validated_opers["delete"]:
            raise InvalidOperation("Delete operations have not been validated")
        return super().delete()

    def _exists(self):
        return super().exists()
    def exists(self):
        if not self.some_oper_validated():
            q = self.can_view()
            self.__dict__.update(q.__dict__)
        return super().exists()

