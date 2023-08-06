from wagtail.admin.menu import Menu, MenuItem

from .permissions import radio_show_permission_policy


class RadioShowMenuItem(MenuItem):
    def is_shown(self, request):
        return radio_show_permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


webradio_menu = Menu(register_hook_name='register_webradio_menu_item')
