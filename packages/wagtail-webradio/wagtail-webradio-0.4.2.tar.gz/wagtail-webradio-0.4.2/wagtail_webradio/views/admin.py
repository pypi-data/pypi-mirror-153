from django.core.exceptions import NON_FIELD_ERRORS, PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wagtail.admin import messages
from wagtail.admin.ui.tables import Column, DateColumn, TitleColumn

from ..forms import podcast_edit_handler, radio_show_edit_handler
from ..models import Podcast, RadioShow
from ..permissions import (
    podcast_permission_policy,
    radio_show_permission_policy,
)
from ..ui import RadioShowPodcastsColumn
from .generic import CreateView, DeleteView, EditView, IndexView

# RADIO SHOWS
# ------------------------------------------------------------------------------


class RadioShowViewMixin:
    model = RadioShow
    permission_policy = radio_show_permission_policy
    index_url_name = 'wagtail_webradio:radioshow_index'
    add_url_name = 'wagtail_webradio:radioshow_add'
    edit_url_name = 'wagtail_webradio:radioshow_edit'
    delete_url_name = 'wagtail_webradio:radioshow_delete'
    header_icon = 'microphone'

    edit_handler = radio_show_edit_handler


class RadioShowIndexView(RadioShowViewMixin, IndexView):
    page_title = _("Radio shows")
    add_item_label = _("Add a radio show")

    @property
    def columns(self):
        return [
            TitleColumn(
                'title', label=gettext("Title"), get_url=self.get_edit_url
            ),
            RadioShowPodcastsColumn('podcasts', get_url=self.get_podcasts_url),
        ]

    def get_queryset(self):
        return self.permission_policy.instances_user_has_any_permission_for(
            self.request.user
        )

    def get_edit_url(self, radio_show):
        if self.permission_policy.user_has_permission_for_instance(
            self.request.user, 'change', radio_show
        ):
            return reverse(self.edit_url_name, args=(radio_show.pk,))

    def get_podcasts_url(self, radio_show):
        if podcast_permission_policy.user_has_any_permission_for_radio_show(
            self.request.user, ['add', 'change', 'delete'], radio_show
        ):
            return reverse(
                'wagtail_webradio:radioshow_podcast_index',
                args=(radio_show.pk,),
            )


class RadioShowCreateView(RadioShowViewMixin, CreateView):
    page_title = _("Add radio show")
    success_message = _("Radio show '{0}' added.")


class RadioShowEditView(RadioShowViewMixin, EditView):
    success_message = _("Radio show '{0}' updated.")
    error_message = _("The radio show could not be saved due to errors.")
    delete_item_label = _("Delete radio show")


class RadioShowDeleteView(RadioShowViewMixin, DeleteView):
    page_title = _("Delete radio show")
    error_message = _("Unable to delete this radio show.")
    success_message = _("Radio show '{0}' deleted.")
    confirmation_message = _("Are you sure you want to delete this radio show?")


# PODCASTS OF A RADIO SHOW
# ------------------------------------------------------------------------------


class PodcastViewMixin:
    model = Podcast
    permission_policy = podcast_permission_policy
    edit_url_name = 'wagtail_webradio:podcast_edit'
    delete_url_name = 'wagtail_webradio:podcast_delete'
    header_icon = 'headphone'

    edit_handler = podcast_edit_handler

    def get_index_url(self):
        return reverse(
            'wagtail_webradio:radioshow_podcast_index',
            args=(self.radio_show.pk,),
        )

    def get_add_url(self):
        if self.permission_policy.user_has_permission_for_radio_show(
            self.request.user, 'add', self.radio_show
        ):
            return reverse(
                'wagtail_webradio:radioshow_podcast_add',
                args=(self.radio_show.pk,),
            )

    def get_success_url(self):
        return self.get_index_url()


class RadioShowPodcastIndexView(PodcastViewMixin, IndexView):
    page_title = _("Podcasts of")
    add_item_label = _("Add a podcast")
    columns = [
        TitleColumn(
            'title',
            label=_("Title"),
            url_name=PodcastViewMixin.edit_url_name,
            sort_key='title',
        ),
        Column(
            'get_duration_display', label=_("Duration"), sort_key='duration'
        ),
        DateColumn(
            'publish_date', label=_("Publish date"), sort_key='publish_date'
        ),
    ]
    # Bypass PermissionCheckedMixin, permission is checked for the radio show
    any_permission_required = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.radio_show = get_object_or_404(
            RadioShow.objects.prefetch_related('podcasts'),
            pk=self.kwargs['radioshow_id'],
        )
        if not self.permission_policy.user_has_any_permission_for_radio_show(
            self.request.user, ['add', 'change', 'delete'], self.radio_show
        ):
            raise PermissionDenied

    def get_queryset(self):
        return self.radio_show.podcasts.all()

    def get_page_subtitle(self):
        return self.radio_show.title


class RadioShowPodcastCreateView(PodcastViewMixin, CreateView):
    page_title = _("Add podcast in")
    success_message = _("Podcast '{0}' added.")
    error_message = _("The podcast could not be created due to errors.")
    # Bypass PermissionCheckedMixin, permission is checked for the radio show
    permission_required = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.radio_show = get_object_or_404(
            RadioShow, pk=self.kwargs['radioshow_id']
        )
        if not self.permission_policy.user_has_permission_for_radio_show(
            self.request.user, 'add', self.radio_show
        ):
            raise PermissionDenied

    def get_form(self):
        form = super().get_form()
        form.instance.radio_show = self.radio_show
        return form

    def get_page_subtitle(self):
        return self.radio_show.title

    def get_error_message(self):
        try:
            non_field_errors = self.form.errors[NON_FIELD_ERRORS]
            for error in non_field_errors:
                messages.error(self.request, error)
        except KeyError:
            return super().get_error_message()


class PodcastEditView(PodcastViewMixin, EditView):
    success_message = _("Podcast '{0}' updated.")
    error_message = _("The podcast could not be saved due to errors.")
    delete_item_label = _("Delete podcast")

    def get_queryset(self):
        return super().get_queryset().select_related('radio_show')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.radio_show = obj.radio_show
        return obj


class PodcastDeleteView(PodcastViewMixin, DeleteView):
    page_title = _("Delete podcast")
    success_message = _("Podcast '{0}' deleted.")
    confirmation_message = _("Are you sure you want to delete this podcast?")

    def get_queryset(self):
        return super().get_queryset().select_related('radio_show')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.radio_show = obj.radio_show
        return obj
