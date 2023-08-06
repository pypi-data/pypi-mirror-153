import json

from django import forms
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail.admin.staticfiles import versioned_static
from wagtail.admin.widgets import AdminChooser
from wagtail.core.telepath import register
from wagtail.core.widget_adapters import WidgetAdapter

from .models import Podcast


class AdminPodcastChooser(AdminChooser):
    choose_one_text = _("Choose a podcast")
    choose_another_text = _("Choose another podcast")
    link_to_chosen_text = _("Edit this podcast")

    def get_value_data(self, value):
        if value is None:
            return None
        elif isinstance(value, Podcast):
            instance = value
        else:  # assume instance ID
            instance = Podcast.objects.get(pk=value)

        return {
            'id': instance.pk,
            'title': instance.title,
            'edit_url': reverse(
                'wagtail_webradio:podcast_edit', args=(instance.pk,)
            ),
        }

    def render_html(self, name, value_data, attrs):
        value_data = value_data or {}

        original_field_html = super().render_html(
            name, value_data.get('id'), attrs
        )

        return render_to_string(
            'wagtail_webradio/widgets/podcast_chooser.html',
            {
                'widget': self,
                'original_field_html': original_field_html,
                'attrs': attrs,
                # only used by chooser.html to identify blank values
                'value': bool(value_data),
                'display_title': value_data.get('title', ''),
                'edit_url': value_data.get('edit_url', ''),
            },
        )

    def render_js_init(self, id_, name, value_data):
        return "createPodcastChooser({0});".format(json.dumps(id_))

    @property
    def media(self):
        return forms.Media(
            js=[
                versioned_static(
                    'wagtail_webradio/admin/js/podcast-chooser-modal.js'
                ),
                versioned_static(
                    'wagtail_webradio/admin/js/podcast-chooser.js'
                ),
            ]
        )


class PodcastChooserAdapter(WidgetAdapter):
    js_constructor = 'wagtail_webradio.widgets.PodcastChooser'

    def js_args(self, widget):
        return [
            widget.render_html('__NAME__', None, attrs={'id': '__ID__'}),
            widget.id_for_label('__ID__'),
        ]

    @cached_property
    def media(self):
        return forms.Media(
            js=[
                versioned_static(
                    'wagtail_webradio/admin/js/podcast-chooser-telepath.js'
                ),
            ]
        )


register(PodcastChooserAdapter(), AdminPodcastChooser)
