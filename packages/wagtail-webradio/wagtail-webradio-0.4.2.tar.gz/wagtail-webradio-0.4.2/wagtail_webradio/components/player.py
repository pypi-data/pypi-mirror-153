from collections import OrderedDict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Union

from django.utils.functional import cached_property

from django_unicorn.components import UnicornView

from ..models import Podcast
from ..utils import format_duration


@dataclass
class Song:
    url: str
    title: str
    subtitle: str
    duration: timedelta = None
    download_url: str = ''
    thumbnail_url: str = ''

    @cached_property
    def duration_str(self):
        return format_duration(self.duration)


class Playlist(Sequence):
    def __init__(self):
        self.data = OrderedDict()
        self._current_id = None
        self._previous_id = None
        self._next_id = None
        self._last_id = 0

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, key) -> Song:
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, key) -> bool:
        return key in self.data

    def __repr__(self):
        return 'Playlist({}, current_id={})'.format(
            self.data,
            self.current_id,
        )

    def items(self):
        return self.data.items()

    def to_json(self):
        return {
            'data': self.data,
            'current_id': self._current_id,
        }

    # Properties

    @property
    def current_id(self) -> Optional[int]:
        """The id of the current song - if any."""
        return self._current_id

    @current_id.setter
    def current_id(self, value: int):
        """Set the id of the current song."""
        if value == self._current_id:
            return
        if value not in self:
            raise KeyError("'%s' is not in the playlist" % value)
        self._current_id = value
        self._update_indexes()

    @current_id.deleter
    def current_id(self):
        """Delete the current song."""
        self._current_id = None
        self._update_indexes()

    @property
    def current(self) -> Optional[Song]:
        """The current `Song` object - if any."""
        return None if self._current_id is None else self[self._current_id]

    @property
    def has_previous(self) -> bool:
        """Whether there is song before the current one."""
        return self._previous_id is not None

    @property
    def has_next(self) -> bool:
        """Whether there is song after the current one."""
        return self._next_id is not None

    # Methods

    def add(self, value: Song) -> int:
        """Add a song at the end of the playlist and return its id."""
        self._last_id += 1
        self.data[self._last_id] = value
        self._update_indexes()
        return self._last_id

    def remove(self, song_id: int):
        """Remove the given song id from the playlist."""
        if song_id not in self:
            raise KeyError("'%s' is not in the playlist" % song_id)
        del self.data[song_id]
        if song_id == self._current_id:
            if self.has_next:
                self.current_id = self._next_id
            elif self.has_previous:
                self.current_id = self._previous_id
            else:
                del self.current_id
        else:
            self._update_indexes()

    def previous(self) -> int:
        """Go to the previous song and return its id."""
        if not self.has_previous:
            raise KeyError("There is no previous song")
        self.current_id = self._previous_id
        return self.current_id

    def next(self) -> int:
        """Go to the next song and return its id."""
        if not self.has_next:
            raise KeyError("There is no next song")
        self.current_id = self._next_id
        return self.current_id

    # Private

    def _update_indexes(self):
        self._previous_id = None
        self._next_id = None
        keys = list(self.data.keys())
        try:
            index = keys.index(self._current_id)
        except ValueError:
            return
        if index > 0:
            self._previous_id = keys[index - 1]
        if index + 1 < len(keys):
            self._next_id = keys[index + 1]


class PlayerView(UnicornView):
    """
    The player component.
    """

    template_name = 'wagtail_webradio/components/player.html'

    #: Whether the current song - if any - must be played.
    autoplay: bool = False

    #: The id of the current song - if any.
    current_id: int = None

    #: The playlist of the player, which can be managed by the actions.
    playlist: Playlist = None

    #: The rendition filter of the thumbnail of a song.
    thumbnail_filter = 'fill-45x45'

    class Meta:
        exclude = ('thumbnail_filter',)
        javascript_exclude = ('current_id', 'playlist')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.playlist = Playlist()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = self.playlist.current
        return context

    # Hooks

    def mount(self):
        self.current_id = self.playlist.current_id

    def updating_current_id(self, value: int):
        try:
            self.playlist.current_id = value
        except KeyError:
            raise AttributeError("This id is not in the playlist")

    # Actions

    def play(self, song_id: int):
        """Play the given song id from the playlist."""
        self._set_property('current_id', song_id)

    def previous(self):
        """Play the previous song in the playlist - if any."""
        try:
            self.current_id = self.playlist.previous()
        except KeyError:
            return

        self.autoplay = True

    def next(self):
        """Play the next song in the playlist - if any."""
        try:
            self.current_id = self.playlist.next()
        except KeyError:
            return

        self.autoplay = True

    def add(self, song: Union[dict, Song], autoplay: bool = True):
        """
        Add the given song to the end of the playlist and play it if `autoplay`
        is given or if there is no current song.
        """
        if isinstance(song, dict):
            song = Song(**song)

        song_id = self.playlist.add(song)

        if self.current_id is None or autoplay:
            self.autoplay = autoplay
            self.play(song_id)

    def add_podcast(self, podcast_id: int, autoplay: bool = True):
        """
        Add the given podcast id to the end of the playlist and play it if
        `autoplay` is given or if there is no current song.
        """
        podcast = self._get_podcast(podcast_id)

        self.add(self._get_song_from_podcast(podcast), autoplay)

    def remove(self, song_id: int):
        """Remove the given song id from the playlist."""
        try:
            self.playlist.remove(song_id)
        except KeyError:
            raise AttributeError("This id is not in the playlist")
        else:
            # set the current song since it could change
            self.current_id = self.playlist.current_id

    def clear(self):
        """Clear the playlist and the current song."""
        self.autoplay = False
        self.playlist = Playlist()
        self.current_id = self.playlist.current_id

    # Private

    def _get_podcast(self, podcast_id: int) -> Podcast:
        return Podcast.objects.get(pk=podcast_id)

    def _get_song_from_podcast(self, podcast: Podcast) -> Song:
        song = Song(
            url=podcast.url,
            title=podcast.title,
            subtitle=podcast.radio_show.title,
            duration=podcast.duration,
            download_url=podcast.url,
        )

        if podcast.picture:
            song.thumbnail_url = podcast.picture.get_rendition(
                self.thumbnail_filter
            ).url

        return song
