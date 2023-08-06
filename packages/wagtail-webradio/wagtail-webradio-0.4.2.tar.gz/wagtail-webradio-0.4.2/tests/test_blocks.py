from django import forms
from django.core.exceptions import ValidationError

from wagtail.core.blocks.field_block import FieldBlockAdapter

import pytest
from pytest_django.asserts import assertInHTML

from wagtail_webradio.blocks import (
    PodcastChooserBlock,
    PodcastTagChooserBlock,
    RadioShowChooserBlock,
)
from wagtail_webradio.widgets import AdminPodcastChooser, PodcastChooserAdapter

from .factories import (
    PodcastFactory,
    RadioShowFactory,
    TagFactory,
    TaggedPodcastFactory,
)


class TestModelChooserBlock:
    def test_form_response(self):
        block = RadioShowChooserBlock()
        radio_show = RadioShowFactory()

        value = block.value_from_datadict(
            {'radio_show': str(radio_show.id)}, {}, 'radio_show'
        )
        assert value == radio_show

        empty_value = block.value_from_datadict(
            {'radio_show': ''}, {}, 'radio_show'
        )
        assert empty_value is None

    def test_clean(self):
        required_block = RadioShowChooserBlock()
        nonrequired_block = RadioShowChooserBlock(required=False)
        radio_show = RadioShowFactory()

        assert required_block.clean(radio_show) == radio_show
        with pytest.raises(ValidationError):
            required_block.clean(None)

        assert nonrequired_block.clean(radio_show) == radio_show
        assert nonrequired_block.clean(None) is None

    def test_widget_choices(self):
        RadioShowFactory.reset_sequence()
        radio_shows = RadioShowFactory.create_batch(2)

        block = RadioShowChooserBlock()
        js_args = FieldBlockAdapter().js_args(block)
        assert [c for c in js_args[1].choices] == [
            ('', '---------'),
            (radio_shows[0].pk, "Radio Show #1"),
            (radio_shows[1].pk, "Radio Show #2"),
        ]


class TestPodcastTagChooserBlock:
    def test_serialize(self):
        block = PodcastTagChooserBlock()
        tag = TaggedPodcastFactory().tag

        assert block.get_prep_value(tag) == tag.id
        assert block.get_prep_value(None) is None

    def test_deserialize(self):
        block = PodcastTagChooserBlock()
        tag = TaggedPodcastFactory().tag

        assert block.to_python(tag.id) == tag
        assert block.to_python(None) is None

    def test_adapt(self):
        block = PodcastTagChooserBlock(help_text="pick a podcast tag")
        block.set_name('test_podcasttagchooserblock')

        js_args = FieldBlockAdapter().js_args(block)
        assert js_args[0] == 'test_podcasttagchooserblock'
        assert type(js_args[1]) is forms.Select
        assert js_args[2] == {
            'label': 'Podcast tag',
            'required': True,
            'icon': 'tag',
            'helpText': 'pick a podcast tag',
            'classname': (
                'field model_choice_field widget-select '
                'fieldname-test_podcasttagchooserblock'
            ),
            'showAddCommentButton': True,
            'strings': {'ADD_COMMENT': 'Add Comment'},
        }

    def test_field_queryset(self):
        block = PodcastTagChooserBlock()
        TaggedPodcastFactory.create_batch(2)
        TagFactory.create_batch(3)

        assert block.field.queryset.count() == 2


class TestRadioShowChooserBlock:
    def test_serialize(self):
        block = RadioShowChooserBlock()
        radio_show = RadioShowFactory()

        assert block.get_prep_value(radio_show) == radio_show.id
        assert block.get_prep_value(None) is None

    def test_deserialize(self):
        block = RadioShowChooserBlock()
        radio_show = RadioShowFactory()

        assert block.to_python(radio_show.id) == radio_show
        assert block.to_python(None) is None

    def test_adapt(self):
        block = RadioShowChooserBlock(help_text="pick a radio show")
        block.set_name('test_radioshowchooserblock')

        js_args = FieldBlockAdapter().js_args(block)
        assert js_args[0] == 'test_radioshowchooserblock'
        assert type(js_args[1]) is forms.Select
        assert js_args[2] == {
            'label': 'Radio show',
            'required': True,
            'icon': 'microphone',
            'helpText': 'pick a radio show',
            'classname': (
                'field model_choice_field widget-select '
                'fieldname-test_radioshowchooserblock'
            ),
            'showAddCommentButton': True,
            'strings': {'ADD_COMMENT': 'Add Comment'},
        }

    def test_field_queryset(self):
        block = RadioShowChooserBlock()
        radio_shows = RadioShowFactory.create_batch(2)

        assert set(block.field.queryset) == set(radio_shows)


class TestPodcastChooserBlock:
    def test_serialize(self):
        block = PodcastChooserBlock()
        podcast = PodcastFactory()

        assert block.get_prep_value(podcast) == podcast.id
        assert block.get_prep_value(None) is None

    def test_deserialize(self):
        block = PodcastChooserBlock()
        podcast = PodcastFactory()

        assert block.to_python(podcast.id) == podcast
        assert block.to_python(None) is None

    def test_adapt(self):
        block = PodcastChooserBlock(help_text="pick a podcast")
        block.set_name('test_podcastchooserblock')

        js_args = FieldBlockAdapter().js_args(block)
        assert js_args[0] == 'test_podcastchooserblock'
        assert type(js_args[1]) is AdminPodcastChooser
        assert js_args[2] == {
            'label': 'Podcast',
            'required': True,
            'icon': 'headphone',
            'helpText': 'pick a podcast',
            'classname': (
                'field model_choice_field widget-admin_podcast_chooser '
                'fieldname-test_podcastchooserblock'
            ),
            'showAddCommentButton': True,
            'strings': {'ADD_COMMENT': 'Add Comment'},
        }

    def test_form_response(self):
        block = PodcastChooserBlock()
        podcast = PodcastFactory()

        value = block.value_from_datadict(
            {'podcast': str(podcast.id)}, {}, 'podcast'
        )
        assert value == podcast

        empty_value = block.value_from_datadict({'podcast': ''}, {}, 'podcast')
        assert empty_value is None

    def test_clean(self):
        required_block = PodcastChooserBlock()
        nonrequired_block = PodcastChooserBlock(required=False)
        podcast = PodcastFactory()

        assert required_block.clean(podcast) == podcast
        with pytest.raises(ValidationError):
            required_block.clean(None)

        assert nonrequired_block.clean(podcast) == podcast
        assert nonrequired_block.clean(None) is None

    def test_widget_adapt(self):
        js_args = PodcastChooserAdapter().js_args(AdminPodcastChooser())
        assertInHTML(
            '<input id="__ID__" name="__NAME__" type="hidden">', js_args[0]
        )
        assert ">Choose a podcast<" in js_args[0]
        assert js_args[1] == '__ID__'

    def test_widget_render_js_init(self):
        widget = AdminPodcastChooser()

        html = widget.render('test', None, {'id': 'test-id'})
        assert 'createPodcastChooser("test-id")' in html

    def test_widget_render_with_value(self):
        podcast = PodcastFactory(title="A foo podcast")
        widget = AdminPodcastChooser()

        html = widget.render('test', podcast, {'id': 'test-id'})
        assertInHTML(
            '<input id="test-id" name="test" type="hidden" value="%d" />'
            % podcast.id,
            html,
        )
        assertInHTML("A foo podcast", html)
        assert 'createPodcastChooser("test-id")' in html
