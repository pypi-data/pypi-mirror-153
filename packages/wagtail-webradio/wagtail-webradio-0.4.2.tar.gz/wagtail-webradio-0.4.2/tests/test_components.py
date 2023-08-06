from datetime import timedelta
from pathlib import Path

from django.test.html import parse_html

import pytest
from wagtail_factories import ImageFactory

from wagtail_webradio.components.player import PlayerView, Playlist

from .factories import PodcastFactory
from .utils import prettify_html

BASE_SNAPSHOT_DIR = Path('tests', 'snapshots')


@pytest.fixture
def player():
    component = PlayerView(component_name='player', component_id='abcd')
    return component


class TestPlaylist:
    def test_iter_items(self):
        song = {
            'title': "The title 1",
            'subtitle': "The sub 1",
            'url': 'https://example.org/1',
        }
        playlist = Playlist()
        playlist.add(song)

        iterator = iter(playlist)
        assert next(iterator) == 1

        for key, value in playlist.items():
            assert key == 1
            assert value == song

    def test_repr_to_json(self):
        playlist = Playlist()
        playlist.add(
            {
                'title': "The title 1",
                'subtitle': "The sub 1",
                'url': 'https://example.org/1',
            }
        )
        playlist.current_id = 1

        assert repr(playlist) == (
            """
Playlist(OrderedDict([(1, {'title': 'The title 1', 'subtitle': 'The sub 1', 'url': 'https://example.org/1'})]), current_id=1)
            """.strip()  # noqa: E501
        )

        assert playlist.to_json() == {
            'data': playlist.data,
            'current_id': 1,
        }


class TestPlayer:
    snapshot_dir = BASE_SNAPSHOT_DIR / 'player'

    @pytest.fixture(autouse=True)
    def setupSnapshot(self, snapshot):
        self.snapshot = snapshot
        self.snapshot.snapshot_dir = self.snapshot_dir

    def assertSnapshotMatch(self, output, file_name):
        self.snapshot.assert_match(prettify_html(parse_html(output)), file_name)

    # Tests

    def test_render(self):
        from django_unicorn.components import UnicornView

        player = UnicornView.create(
            component_id='xyz',
            component_name='player',
        )
        self.assertSnapshotMatch(player.render(), 'empty.html')

        player.add(
            {
                'title': "The title 1",
                'subtitle': "The sub 1",
                'url': 'https://example.org/1',
            }
        )
        player.add(
            {
                'title': "The title 2",
                'subtitle': "The sub 2",
                'url': 'https://example.org/2',
            },
            False,
        )
        self.assertSnapshotMatch(player.render(), 'with_playlist.html')

    def test_methods(self, player):
        assert set(player._methods().keys()) == {
            'add',
            'add_podcast',
            'remove',
            'clear',
            'play',
            'previous',
            'next',
        }

    def test_add(self, player):
        player.clear()
        player.add(
            {
                'title': "The title",
                'subtitle': "The sub",
                'url': 'https://example.org',
            }
        )

        assert len(player.playlist) == 1
        assert player.current_id == player.playlist.current_id == 1
        assert player.playlist.current.url == 'https://example.org'
        assert player.autoplay is True

    def test_add_no_autoplay(self, player):
        player.clear()
        player.add(
            {
                'title': "The title",
                'subtitle': "The sub",
                'url': 'https://example.org',
            },
            False,
        )

        assert len(player.playlist) == 1
        assert player.current_id == 1
        assert player.autoplay is False

        player.add(
            {
                'title': "The title",
                'subtitle': "The sub",
                'url': 'https://example.org',
            },
            False,
        )

        assert len(player.playlist) == 2
        assert player.current_id == 1
        assert player.autoplay is False

    def test_add_podcast(self, player):
        player.clear()
        podcast = PodcastFactory(
            title="The podcast",
            radio_show__title="The show",
            sound_url='https://example.org',
            duration=timedelta(minutes=3, seconds=10),
        )

        player.add_podcast(podcast.pk)

        song = player.playlist.current
        assert song.title == "The podcast"
        assert song.subtitle == "The show"
        assert song.url == 'https://example.org'
        assert song.duration_str == '03:10'
        assert song.download_url == 'https://example.org'
        assert song.thumbnail_url == ''

        podcast.picture = ImageFactory()
        podcast.save()

        player.add_podcast(podcast.pk)

        song = player.playlist.current
        assert song.thumbnail_url != ''

    def test_remove(self, player):
        player.clear()
        player.add(
            {
                'title': "The title 1",
                'subtitle': "The sub 1",
                'url': 'https://example.org/1',
            }
        )
        player.add(
            {
                'title': "The title 2",
                'subtitle': "The sub 2",
                'url': 'https://example.org/2',
            }
        )
        player.add(
            {
                'title': "The title 3",
                'subtitle': "The sub 3",
                'url': 'https://example.org/3',
            },
            False,
        )
        player.add(
            {
                'title': "The title 4",
                'subtitle': "The sub 4",
                'url': 'https://example.org/4',
            },
            False,
        )

        # -> { 1, [2], 3, 4 }
        assert player.current_id == 2
        assert player.playlist.has_previous is True
        assert player.playlist.has_next is True

        player.remove(4)  # -> { 1, [2], 3 }
        assert player.current_id == 2
        assert player.playlist.has_previous is True
        assert player.playlist.has_next is True

        player.remove(2)  # -> { 1, [3] }
        assert player.current_id == 3
        assert player.playlist.has_previous is True
        assert player.playlist.has_next is False

        player.remove(3)  # -> { [1] }
        assert player.current_id == 1
        assert player.playlist.has_previous is False
        assert player.playlist.has_next is False

        player.remove(1)  # -> {}
        assert player.current_id is None
        assert player.playlist.has_previous is False
        assert player.playlist.has_next is False

        with pytest.raises(AttributeError):
            player.remove(1)

    def test_previous_next(self, player):
        player.clear()
        player.add(
            {
                'title': "The title 1",
                'subtitle': "The sub 1",
                'url': 'https://example.org/1',
            }
        )
        player.add(
            {
                'title': "The title 2",
                'subtitle': "The sub 2",
                'url': 'https://example.org/2',
            },
            False,
        )

        assert player.current_id == 1

        player.autoplay = False
        player.next()
        assert player.current_id == 2
        assert player.autoplay is True

        player.next()
        assert player.current_id == 2

        player.autoplay = False
        player.previous()
        assert player.current_id == 1
        assert player.autoplay is True

        player.previous()
        assert player.current_id == 1

    def test_play(self, player):
        player.clear()
        player.add(
            {
                'title': "The title 1",
                'subtitle': "The sub 1",
                'url': 'https://example.org/1',
            }
        )
        player.add(
            {
                'title': "The title 2",
                'subtitle': "The sub 2",
                'url': 'https://example.org/2',
            },
            False,
        )

        assert player.current_id == 1

        player.play(2)
        assert player.current_id == 2

        player.play(2)
        assert player.current_id == 2

        with pytest.raises(AttributeError):
            player.play(3)
        assert player.current_id == 2
