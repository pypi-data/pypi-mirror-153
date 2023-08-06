from django.contrib import admin

class GuardianAdminMixin:
    def save_model(self, request, obj, form, change):
        obj._save()

    def get_queryset(self, request):
        return super().get_queryset(request).is_owner()

    def get_field_queryset(self, db, db_field, request):
        """
        If the ModelAdmin specifies ordering, the queryset should respect that
        ordering.  Otherwise don't specify the queryset, let the field decide
        (return None in that case).
        """
        related_admin = self.admin_site._registry.get(db_field.remote_field.model)
        if related_admin is not None:
            ordering = related_admin.get_ordering(request)
            queryset = db_field.remote_field.model._default_manager.using(db)
            if ordering is not None and ordering != ():
                queryset = queryset.order_by(*ordering)
            try:
                return queryset.can_view()
            except:
                return queryset
        return None

    # def get_queryset(self, request):
    #     # use our manager, rather than the default one
    #     qs = self.model._objects.get_queryset()
    #
    #     # we need this from the superclass method
    #     ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
    #     if ordering:
    #         qs = qs.order_by(*ordering)
    #     return qs

class GuardianModelAdmin(GuardianAdminMixin, admin.ModelAdmin):
    pass