from django.urls import path

from .views import admin, chooser

app_name = 'wagtail_webradio'

urlpatterns = [
    path(
        'radioshow/',
        admin.RadioShowIndexView.as_view(),
        name='radioshow_index',
    ),
    path(
        'radioshow/add/',
        admin.RadioShowCreateView.as_view(),
        name='radioshow_add',
    ),
    path(
        'radioshow/<int:pk>/',
        admin.RadioShowEditView.as_view(),
        name='radioshow_edit',
    ),
    path(
        'radioshow/<int:pk>/delete/',
        admin.RadioShowDeleteView.as_view(),
        name='radioshow_delete',
    ),
    path(
        'radioshow/<int:radioshow_id>/podcast/',
        admin.RadioShowPodcastIndexView.as_view(),
        name='radioshow_podcast_index',
    ),
    path(
        'radioshow/<int:radioshow_id>/podcast/add/',
        admin.RadioShowPodcastCreateView.as_view(),
        name='radioshow_podcast_add',
    ),
    path(
        'podcast/chooser/',
        chooser.PodcastChooseView.as_view(),
        name='podcast_chooser',
    ),
    path(
        'podcast/chooser/results/',
        chooser.PodcastChooseResultsView.as_view(),
        name='podcast_chooser_results',
    ),
    path(
        'podcast/chooser/<int:pk>/',
        chooser.podcast_chosen,
        name='podcast_chosen',
    ),
    path(
        'podcast/<int:pk>/',
        admin.PodcastEditView.as_view(),
        name='podcast_edit',
    ),
    path(
        'podcast/<int:pk>/delete/',
        admin.PodcastDeleteView.as_view(),
        name='podcast_delete',
    ),
]
