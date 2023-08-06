import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.files import File

from wagtail.core.models import Site

import pytest

from wagtail_webradio.models import GroupRadioShowPermission

from .factories import PodcastFactory, RadioShowFactory

AUDIO_SINE_PATH = os.path.join(os.path.dirname(__file__), 'data/sine.ogg')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def change_radioshow_perm():
    return Permission.objects.get(codename='change_radioshow')


@pytest.fixture
def add_podcast_perm():
    return Permission.objects.get(codename='add_podcast')


@pytest.fixture
def change_podcast_perm():
    return Permission.objects.get(codename='change_podcast')


@pytest.fixture
def delete_podcast_perm():
    return Permission.objects.get(codename='delete_podcast')


@pytest.fixture
def manager_radio_shows():
    return RadioShowFactory.create_batch(4)


@pytest.fixture
def manager_group(
    manager_radio_shows,
    change_radioshow_perm,
    add_podcast_perm,
    change_podcast_perm,
    delete_podcast_perm,
):
    group = Group.objects.create(name="Radio show's manager")
    group.permissions.add(Permission.objects.get(codename='access_admin'))

    # Create the following permissions on manager_radio_shows:
    #  0. change_radioshow, add_podcast, change_podcast
    GroupRadioShowPermission.objects.create(
        group=group,
        radio_show=manager_radio_shows[0],
        permission=change_radioshow_perm,
    )
    GroupRadioShowPermission.objects.create(
        group=group,
        radio_show=manager_radio_shows[0],
        permission=add_podcast_perm,
    )
    GroupRadioShowPermission.objects.create(
        group=group,
        radio_show=manager_radio_shows[0],
        permission=change_podcast_perm,
    )
    #  1. change_radioshow
    GroupRadioShowPermission.objects.create(
        group=group,
        radio_show=manager_radio_shows[1],
        permission=change_radioshow_perm,
    )
    #  2. add_podcast, change_podcast, delete_podcast
    GroupRadioShowPermission.objects.create(
        group=group,
        radio_show=manager_radio_shows[2],
        permission=add_podcast_perm,
    )
    GroupRadioShowPermission.objects.create(
        group=group,
        radio_show=manager_radio_shows[2],
        permission=change_podcast_perm,
    )
    GroupRadioShowPermission.objects.create(
        group=group,
        radio_show=manager_radio_shows[2],
        permission=delete_podcast_perm,
    )

    return group


@pytest.fixture
def manager_user(manager_group):
    user = get_user_model().objects.create_user('manager', 'manager@no.lan')
    user.groups.add(manager_group)
    return user


@pytest.fixture
def home_page():
    return Site.objects.get(is_default_site=True).root_page


@pytest.fixture
def podcast_file():
    podcast = PodcastFactory.create(
        sound_file=File(open(AUDIO_SINE_PATH, 'rb')),
        sound_url='',
    )
    yield podcast
    # delete also the underlying file
    podcast.sound_file.delete()
