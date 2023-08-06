from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from wagtail.admin.ui.tables import Column


class RadioShowPodcastsColumn(Column):
    cell_template_name = 'wagtail_webradio/tables/radio_show_podcasts_cell.html'

    class Media:
        css = {
            'screen': [
                'wagtail_webradio/admin/css/radio_show_podcasts_cell.css'
            ]
        }

    def __init__(self, name, get_url):
        super().__init__(name, label=_("Podcasts"))
        self._get_url_func = get_url

    def render_header_html(self, parent_context):
        return mark_safe('<th class="radioshow-podcasts"></th>')

    def get_cell_context_data(self, instance, parent_context):
        return {
            'column': self,
            'instance': instance,
            'podcasts_url': self._get_url_func(instance),
            'request': parent_context.get('request'),
        }
