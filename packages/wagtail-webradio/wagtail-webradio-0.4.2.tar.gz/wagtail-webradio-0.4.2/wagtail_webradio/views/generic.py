from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.urls import reverse
from django.utils.text import capfirst
from django.utils.translation import gettext as _

from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.views import generic


class EditHandlerFormViewMixin:
    #: The edit handler object to use for the model.
    edit_handler = None

    def get_instance(self):
        return getattr(self, 'object') or self.model()

    def get_edit_handler(self):
        return self.edit_handler.bind_to(
            instance=self.get_instance(), request=self.request
        )

    def get_form(self):
        edit_handler = self.get_edit_handler()
        form = super().get_form(edit_handler.get_form_class())
        # Save the new edit handler object which is now bound
        self.edit_handler = edit_handler.bind_to(form=form)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_handler'] = self.edit_handler
        return context


class InstancePermissionCheckedMixin:
    permission_required = None
    any_permission_required = None

    #: Any action the user must be allowed to perform on the instance.
    instance_any_permission_required = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert self.instance_any_permission_required, (
            "instance_any_permission_required must be defined by the view to "
            "use InstancePermissionCheckedMixin"
        )

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        if not self.permission_policy.user_has_any_permission_for_instance(
            self.request.user, self.instance_any_permission_required, instance
        ):
            raise PermissionDenied

        return instance


class IndexView(generic.IndexView):
    template_name = 'wagtail_webradio/generic/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # FIXME: https://github.com/wagtail/wagtail/pull/7657
        if context['can_add']:
            context['add_url'] = self.get_add_url()
            context['add_item_label'] = self.add_item_label
        return context

    def get_add_url(self):
        # FIXME: https://github.com/wagtail/wagtail/pull/7657
        if self.add_url_name:
            return reverse(self.add_url_name)


class CreateView(EditHandlerFormViewMixin, generic.CreateView):
    template_name = 'wagtail_webradio/generic/create.html'


class EditView(
    InstancePermissionCheckedMixin, EditHandlerFormViewMixin, generic.EditView
):
    template_name = 'wagtail_webradio/generic/edit.html'
    instance_any_permission_required = ['change']


class DeleteView(InstancePermissionCheckedMixin, generic.DeleteView):
    template_name = 'wagtail_webradio/generic/confirm_delete.html'
    instance_any_permission_required = ['delete']

    #: An optional error message to display when there is protected relation.
    error_message = None

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            context = self.get_context_data(
                protected_objects=self.format_protected_objects(
                    e.protected_objects
                )
            )
            return self.render_to_response(context)

    def format_protected_objects(self, objects):
        """
        Generate a list of 2-tuple with the string describing the object and
        its admin edit URL from the one which have a protected relation to the
        item to delete.
        """
        url_finder = AdminURLFinder(self.request.user)

        return [
            (
                _('{model}: {object}').format(
                    model=capfirst(obj.__class__._meta.verbose_name), object=obj
                ),
                url_finder.get_edit_url(obj),
            )
            for obj in objects
        ]
