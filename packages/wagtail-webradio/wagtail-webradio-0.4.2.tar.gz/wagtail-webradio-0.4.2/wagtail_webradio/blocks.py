from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks
from wagtail.core.utils import resolve_model_string


class ModelChooserBlock(blocks.ChooserBlock):
    @cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.get_queryset(),
            widget=self.widget,
            required=self._required,
            validators=self._validators,
            help_text=self._help_text,
        )

    @cached_property
    def widget(self):
        return forms.Select()

    @cached_property
    def target_model(self):
        raise NotImplementedError

    def get_queryset(self):
        return self.target_model.objects.all()

    def value_from_form(self, value):
        if value == '':
            return None
        return super().value_from_form(value)


class RadioShowChooserBlock(ModelChooserBlock):
    class Meta:
        label = _("Radio show")
        icon = 'microphone'

    @cached_property
    def target_model(self):
        return resolve_model_string('wagtail_webradio.RadioShow')


class PodcastTagChooserBlock(ModelChooserBlock):
    class Meta:
        label = _("Podcast tag")
        icon = 'tag'

    @cached_property
    def tagged_model(self):
        return resolve_model_string('wagtail_webradio.TaggedPodcast')

    @cached_property
    def target_model(self):
        return self.tagged_model.tag_model()

    def get_queryset(self):
        return self.tagged_model.tags_for()


class PodcastChooserBlock(blocks.ChooserBlock):
    class Meta:
        label = _("Podcast")
        icon = 'headphone'

    @cached_property
    def target_model(self):
        return resolve_model_string('wagtail_webradio.Podcast')

    @cached_property
    def widget(self):
        from wagtail_webradio.widgets import AdminPodcastChooser

        return AdminPodcastChooser()

    def get_form_state(self, value):
        value_data = self.widget.get_value_data(value)
        if value_data is None:
            return None
        else:
            return {
                'id': value_data['id'],
                'edit_link': value_data['edit_url'],
                'title': value_data['title'],
            }
