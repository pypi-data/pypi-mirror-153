from django.contrib.auth.models import Permission
from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _

from wagtail.admin.admin_url_finder import (
    ModelAdminURLFinder,
    register_admin_url_finder,
)
from wagtail.admin.menu import SubmenuMenuItem
from wagtail.core import hooks

from . import admin_urls
from .forms import GroupRadioShowPermissionFormSet
from .menu import RadioShowMenuItem, webradio_menu
from .models import Podcast, RadioShow
from .permissions import podcast_permission_policy, radio_show_permission_policy


@hooks.register('register_admin_menu_item')
def register_webradio_menu():
    return SubmenuMenuItem(
        _("Web radio"),
        webradio_menu,
        icon_name='broadcast',
        order=410,
    )


@hooks.register('register_webradio_menu_item')
def register_radio_shows_menu_item():
    return RadioShowMenuItem(
        _("Radio shows"),
        reverse('wagtail_webradio:radioshow_index'),
        icon_name='microphone',
        order=10,
    )


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [path('webradio/', include(admin_urls))]


@hooks.register('register_icons')
def register_icons(icons):
    for icon in ['broadcast', 'headphone', 'microphone']:
        icons.append('wagtail_webradio/icons/{}.svg'.format(icon))
    return icons


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label='wagtail_webradio',
        codename__in=[
            'add_podcast',
            'change_podcast',
            'delete_podcast',
            'add_radioshow',
            'change_radioshow',
            'delete_radioshow',
        ],
    )


@hooks.register('register_group_permission_panel')
def register_radio_show_permissions_panel():
    return GroupRadioShowPermissionFormSet


class PodcastAdminURLFinder(ModelAdminURLFinder):
    permission_policy = podcast_permission_policy
    edit_url_name = 'wagtail_webradio:podcast_edit'


class RadioShowAdminURLFinder(ModelAdminURLFinder):
    permission_policy = radio_show_permission_policy
    edit_url_name = 'wagtail_webradio:radioshow_edit'


register_admin_url_finder(Podcast, PodcastAdminURLFinder)
register_admin_url_finder(RadioShow, RadioShowAdminURLFinder)
