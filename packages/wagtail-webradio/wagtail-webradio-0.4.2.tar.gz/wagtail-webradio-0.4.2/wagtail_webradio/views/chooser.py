from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.base import View

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.ui.tables import Column, DateColumn, Table, TitleColumn

from ..forms import PodcastChooserSearchForm
from ..models import Podcast


class BasePodcastChooseView(View):
    columns = [
        TitleColumn(
            'title',
            label=_("Title"),
            url_name='wagtail_webradio:podcast_chosen',
        ),
        Column('radio_show', label=_("Radio show")),
        DateColumn('publish_date', label=_("Publish date")),
    ]
    search_form_class = PodcastChooserSearchForm

    def get(self, request):
        objects = Podcast.objects.all()

        self.search_form = self.search_form_class(
            **self.get_search_form_kwargs()
        )
        self.is_searching = (
            self.search_form.is_bound and self.search_form.is_valid()
        )

        if self.is_searching:
            objects = self.search_form.filter(objects)
        else:
            objects = objects.order_by('-publish_date')

        paginator = Paginator(objects, per_page=10)
        self.objects = paginator.get_page(request.GET.get('p'))

        self.table = Table(self.columns, self.objects)

        return self.render_to_response()

    def get_context_data(self):
        return {
            'objects': self.objects,
            'table': self.table,
            'search_form': self.search_form,
            'is_searching': self.is_searching,
        }

    def render_to_response(self):
        raise NotImplementedError()

    def get_search_form_kwargs(self):
        kwargs = {}

        if any(
            field_name in self.request.GET
            for field_name in self.search_form_class.base_fields.keys()
        ):
            kwargs['data'] = self.request.GET

        return kwargs


class PodcastChooseView(BasePodcastChooseView):
    def render_to_response(self):
        return render_modal_workflow(
            self.request,
            'wagtail_webradio/chooser/podcast_chooser.html',
            None,
            self.get_context_data(),
            json_data={
                'step': 'choose',
                'error_label': _("Server Error"),
                'error_message': _(
                    "Report this error to your website administrator with the "
                    "following information:"
                ),
            },
        )


class PodcastChooseResultsView(BasePodcastChooseView):
    def render_to_response(self):
        return TemplateResponse(
            self.request,
            'wagtail_webradio/chooser/podcast_results.html',
            self.get_context_data(),
        )


def podcast_chosen(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk)

    return render_modal_workflow(
        request,
        None,
        None,
        None,
        json_data={
            'step': 'chosen',
            'result': {
                'id': podcast.id,
                'title': podcast.title,
                'edit_link': reverse(
                    'wagtail_webradio:podcast_edit', args=(podcast.id,)
                ),
            },
        },
    )
