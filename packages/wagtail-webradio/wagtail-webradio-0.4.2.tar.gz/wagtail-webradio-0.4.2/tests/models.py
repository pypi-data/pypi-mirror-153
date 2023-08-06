from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtail_webradio.blocks import (
    PodcastChooserBlock,
    PodcastTagChooserBlock,
    RadioShowChooserBlock,
)


class TestPage(Page):
    body = StreamField(
        [
            ('podcast', PodcastChooserBlock()),
            ('podcast_tag', PodcastTagChooserBlock()),
            ('radio_show', RadioShowChooserBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
