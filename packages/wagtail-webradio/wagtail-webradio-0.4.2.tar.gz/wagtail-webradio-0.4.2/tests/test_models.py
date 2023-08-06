import datetime
import os

from django.contrib.auth.models import Group
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.utils import timezone

import pytest
from freezegun import freeze_time

from wagtail_webradio.models import GroupRadioShowPermission, Podcast

from .factories import ImageFactory, PodcastFactory, RadioShowFactory

AUDIO_SINE_PATH = os.path.join(os.path.dirname(__file__), 'data/sine.ogg')


class TestAutoSlugMixin:
    def test_radioshow_slug(self):
        radioshow = RadioShowFactory.build(title="Ûnicode Show")
        assert radioshow.slug == ''

        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'unicode-show'

    def test_poadcast_slug(self):
        podcast = PodcastFactory.build(
            title="Ûnicode Podcast", radio_show=RadioShowFactory()
        )
        assert podcast.slug == ''

        podcast.full_clean()
        podcast.save()
        assert podcast.slug == 'unicode-podcast'

    def test_generated_slug_update(self):
        radioshow = RadioShowFactory.build(title="A simple Show")
        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'a-simple-show'

        radioshow.slug = ''
        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'a-simple-show'

    def test_generated_slug_suffix(self):
        radioshow = RadioShowFactory.build(title="A simple Show")
        radioshow.full_clean()
        radioshow.save()
        assert radioshow.slug == 'a-simple-show'

        radioshow1 = RadioShowFactory.build(title="a Simple show")
        radioshow1.full_clean()
        assert radioshow1.slug == 'a-simple-show-1'

    def test_empty_base_slug(self):
        radioshow = RadioShowFactory.build(title="")

        with pytest.raises(ValidationError) as exc_info:
            radioshow.full_clean()
        assert set(exc_info.value.error_dict.keys()) == {'title', 'slug'}

    def test_slug_unavailable(self):
        RadioShowFactory(title="A simple Show")

        radioshow = RadioShowFactory.build(
            title="A simple Show", slug='a-simple-show'
        )
        with pytest.raises(ValidationError) as exc_info:
            radioshow.full_clean()
        assert set(exc_info.value.error_dict.keys()) == {'slug'}
        assert "already in use" in exc_info.value.messages[0]


class TestGroupRadioShowPermission:
    def test_natural_key(self, change_radioshow_perm):
        group = Group.objects.create(name="A group")
        radio_show = RadioShowFactory()

        obj = GroupRadioShowPermission.objects.create(
            group=group,
            radio_show=radio_show,
            permission=change_radioshow_perm,
        )

        assert obj.natural_key() == (group, radio_show, change_radioshow_perm)
        assert (
            GroupRadioShowPermission.objects.get_by_natural_key(
                group, radio_show, change_radioshow_perm
            )
            == obj
        )


class TestPodcast:
    def test_no_picture(self):
        podcast = PodcastFactory.build()
        assert podcast.get_picture() is None

    def test_has_picture(self):
        podcast = PodcastFactory.build(
            radio_show=RadioShowFactory(
                picture=ImageFactory(title="RadioShow image")
            ),
            picture=ImageFactory(title="Podcast image"),
        )
        assert podcast.get_picture().title == "Podcast image"

    def test_fallback_radioshow_picture(self):
        podcast = PodcastFactory.build(
            radio_show=RadioShowFactory(
                picture=ImageFactory(title="RadioShow image")
            ),
        )
        assert podcast.get_picture().title == "RadioShow image"

    def test_currents_queryset(self):
        with freeze_time(datetime.datetime(2022, 3, 24, 1)):
            for title, delta in [
                ("yesterday", -1),
                ("today", 0),
                ('tomorrow', 1),
            ]:
                PodcastFactory.create(
                    title=title,
                    publish_date=timezone.now()
                    + datetime.timedelta(days=delta),
                )
            currents_titles = [p.title for p in Podcast.objects.currents()]
            assert 'yesterday' in currents_titles
            assert 'today' in currents_titles
            assert 'tomorrow' not in currents_titles

    def test_at_least_one_sound(self):
        with pytest.raises(ValidationError) as exc_infos:
            PodcastFactory.create(sound_url='', sound_file=None)
        assert (
            exc_infos.value.error_dict[NON_FIELD_ERRORS][0].message
            == "You must fill at least a sound file or a sound url"
        )

    def test_only_one_sound(self):
        with pytest.raises(ValidationError) as exc_infos:
            PodcastFactory.create(
                sound_url="https://good.url/sound.mp3",
                sound_file=File(open(AUDIO_SINE_PATH, 'rb')),
            )
        assert (
            exc_infos.value.error_dict[NON_FIELD_ERRORS][0].message
            == "Only one sound must be set (file or url)"
        )

    def test_sound_path(self, podcast_file):
        assert podcast_file.sound_file.path == '{}/{}'.format(
            os.path.dirname(__file__),
            f'var/media/podcasts/{podcast_file.slug}.ogg',
        )

    def test_sound_not_valid(self):
        with pytest.raises(ValidationError) as exc_infos:
            PodcastFactory.create(
                sound_url='', sound_file=ContentFile('', name='file.txt')
            )
        assert exc_infos.value.error_dict['sound_file'][0].message == (
            "The file type application/x-empty is not authorized. "
            "Authorized file types are audio/ogg, audio/mpeg, audio/flac, "
            "audio/opus."
        )

    def test_sound_valid(self, podcast_file):
        assert podcast_file

    def test_file_url(self, podcast_file):
        assert podcast_file.url == podcast_file.sound_file.url

    def test_external_url(self):
        podcast = PodcastFactory.create(sound_url="https://good.url/sound.mp3")
        assert podcast.url == 'https://good.url/sound.mp3'
