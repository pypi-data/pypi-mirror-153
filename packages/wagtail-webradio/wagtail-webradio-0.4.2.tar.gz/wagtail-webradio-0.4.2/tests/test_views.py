import datetime
from html import escape

from django.contrib.auth.models import Group, Permission
from django.core.exceptions import NON_FIELD_ERRORS
from django.urls import reverse
from django.utils.timezone import make_naive

import pytest
from bs4 import BeautifulSoup
from webtest import Upload

from wagtail_webradio.models import GroupRadioShowPermission, Podcast, RadioShow

from .factories import PodcastFactory, RadioShowFactory
from .models import TestPage
from .utils import (
    AdminViewTestMixin,
    ViewTestMixin,
    add_form_data,
    add_inline_form_data,
    get_streamfield_form_data,
)


class TestPageBlocks(AdminViewTestMixin):
    def test_add_and_edit(self, home_page):
        podcast = PodcastFactory(
            title="foopodcast", radio_show__title="fooradioshow"
        )

        form = self.get(
            reverse(
                'wagtailadmin_pages:add',
                args=(
                    TestPage._meta.app_label,
                    TestPage._meta.model_name,
                    home_page.pk,
                ),
            )
        ).forms[1]

        form['title'] = "Test page"
        form['slug'] = 'test-page'
        add_form_data(
            form,
            get_streamfield_form_data(
                'body',
                [
                    ('podcast', podcast.pk),
                    ('radio_show', podcast.radio_show_id),
                ],
            ),
        )
        form.submit(status=302).follow()

        page = TestPage.objects.get(slug='test-page')

        response = self.get(
            reverse('wagtailadmin_pages:edit', args=(page.pk,)),
            status=200,
        )
        assert "foopodcast" in response
        assert "fooradioshow" in response


class RadioShowAdminViewsMixin:
    index_url = reverse('wagtail_webradio:radioshow_index')
    add_url = reverse('wagtail_webradio:radioshow_add')

    def get_edit_url(self, obj):
        return reverse('wagtail_webradio:radioshow_edit', args=(obj.pk,))

    def get_delete_url(self, obj):
        return reverse('wagtail_webradio:radioshow_delete', args=(obj.pk,))

    def get_podcasts_url(self, obj):
        return reverse(
            'wagtail_webradio:radioshow_podcast_index', args=(obj.pk,)
        )


class TestRadioShowAdminViews(RadioShowAdminViewsMixin, AdminViewTestMixin):
    def test_index(self):
        RadioShowFactory.reset_sequence()
        RadioShowFactory()
        PodcastFactory.create_batch(2, radio_show=RadioShowFactory())

        html = self.get(self.index_url, status=200).html
        assert html.find(
            'link',
            href=(
                '/static/wagtail_webradio/admin/css/'
                'radio_show_podcasts_cell.css'
            ),
        )
        assert html.find('a', href=self.add_url).text == "Add a radio show"
        rows = html.select('table.listing tbody > tr')
        assert len(rows) == 2
        cells = rows[0].select('td')
        assert len(cells) == 2
        assert cells[0].find(
            'a',
            string="Radio Show #1",
            href='/admin/webradio/radioshow/1/',
        )
        assert cells[1].find(
            'a',
            title="View podcasts of 'Radio Show #1'",
            href='/admin/webradio/radioshow/1/podcast/',
        )

    def test_add(self):
        response = self.get(self.add_url)
        assert "Add radio show" in response
        form = response.forms[1]
        assert form.action == self.add_url

        form['title'] = "The Voice Without Master"
        form['description'] = (
            response.context['form']
            .fields['description']
            .widget.format_value("<p>Description of this radio show.</p>")
        )
        form['contact_email'] = 'voice@example.org'
        response = form.submit(status=302)
        assert response['location'] == self.index_url
        assert escape("'The Voice Without Master' added") in response.follow()

        radio_show = RadioShow.objects.get(title="The Voice Without Master")
        assert radio_show.contact_email == 'voice@example.org'
        assert radio_show.slug == 'the-voice-without-master'

    def test_edit(self):
        radio_show = RadioShowFactory()
        url = self.get_edit_url(radio_show)

        form = self.get(url).forms[1]
        form['title'] = "The Voice Without Master"
        form['contact_phone'] = '+33310101010'
        response = form.submit(status=302)
        assert response['location'] == self.index_url
        assert escape("'The Voice Without Master' updated") in response.follow()

        radio_show.refresh_from_db()
        radio_show.contact_phone == '+33310101010'

    def test_delete(self):
        radio_show = RadioShowFactory()
        url = self.get_delete_url(radio_show)

        delete_form = self.get(url, status=200).forms[1]
        assert delete_form.action == url

        delete_form.submit().follow(status=200)
        assert not RadioShow.objects.filter(pk=radio_show.pk).exists()

    def test_delete_protected_podcasts(self):
        radio_show = RadioShowFactory()
        podcast = PodcastFactory(title="A podcast", radio_show=radio_show)
        url = self.get_delete_url(radio_show)

        delete_form = self.get(url, status=200).forms[1]
        html = delete_form.submit(status=200).html
        links = html.select('form .listing li a')
        assert len(links) == 1
        assert links[0].string == 'Podcast: A podcast'
        assert links[0].attrs['href'] == reverse(
            'wagtail_webradio:podcast_edit', args=(podcast.pk,)
        )


class TestRadioShowAdminManagerViews(RadioShowAdminViewsMixin, ViewTestMixin):
    @pytest.fixture(autouse=True)
    def setup_user(self, manager_user):
        self.user = manager_user

    def test_index(self, manager_radio_shows):
        html = self.get(self.index_url, status=200).html
        assert not html.find('a', href=self.add_url)
        rows = html.select('table.listing tbody > tr')
        assert len(rows) == 3
        # 0. edit & podcasts
        assert rows[0].find('a', href=self.get_edit_url(manager_radio_shows[0]))
        assert rows[0].find(
            'a', href=self.get_podcasts_url(manager_radio_shows[0])
        )
        # 1. edit
        assert rows[1].find('a', href=self.get_edit_url(manager_radio_shows[1]))
        assert not rows[1].find(
            'a', href=self.get_podcasts_url(manager_radio_shows[1])
        )
        # 2. podcasts
        assert not rows[2].find(
            'a', href=self.get_edit_url(manager_radio_shows[2])
        )
        assert rows[2].find(
            'a', href=self.get_podcasts_url(manager_radio_shows[2])
        )

    def test_index_with_user_permissions(
        self, manager_radio_shows, add_podcast_perm
    ):
        radio_show = RadioShowFactory()
        self.user.user_permissions.add(add_podcast_perm)

        html = self.get(self.index_url, status=200).html
        rows = html.select('table.listing tbody > tr')
        assert len(rows) == len(manager_radio_shows) + 1
        assert not rows[-1].find('a', href=self.get_edit_url(radio_show))
        assert rows[-1].find('a', href=self.get_podcasts_url(radio_show))

    def test_add_unauthorized(self):
        self.get(self.add_url, status=302)

    def test_edit(self, manager_radio_shows):
        self.get(self.get_edit_url(manager_radio_shows[0]), status=200)

    def test_edit_unauthorized(self, manager_radio_shows):
        self.get(self.get_edit_url(manager_radio_shows[2]), status=302)

    def test_delete_unauthorized(self, manager_radio_shows):
        self.get(self.get_delete_url(manager_radio_shows[0]), status=302)


class PodcastAdminViewsMixin:
    def get_index_url(self, radio_show):
        return reverse(
            'wagtail_webradio:radioshow_podcast_index', args=(radio_show.pk,)
        )

    def get_add_url(self, radio_show):
        return reverse(
            'wagtail_webradio:radioshow_podcast_add', args=(radio_show.pk,)
        )

    def get_edit_url(self, obj):
        return reverse('wagtail_webradio:podcast_edit', args=(obj.pk,))

    def get_delete_url(self, obj):
        return reverse('wagtail_webradio:podcast_delete', args=(obj.pk,))


class TestPodcastAdminViews(PodcastAdminViewsMixin, AdminViewTestMixin):
    def test_index(self):
        PodcastFactory.reset_sequence()
        radio_show = RadioShowFactory()
        PodcastFactory.create_batch(2, radio_show=radio_show)
        PodcastFactory(
            duration=datetime.timedelta(minutes=3), radio_show=radio_show
        )
        PodcastFactory()

        html = self.get(self.get_index_url(radio_show), status=200).html
        assert html.find('a', href=self.get_add_url(radio_show)).text == (
            "Add a podcast"
        )
        rows = html.select('table.listing tbody > tr')
        assert len(rows) == 3
        cells = rows[0].select('td')
        assert len(cells) == 3
        assert cells[0].find(
            'a',
            string="Podcast #3",
            href='/admin/webradio/podcast/3/',
        )
        assert cells[1].string.strip() == '03:00'

    def test_add(self):
        radio_show = RadioShowFactory()
        add_url = self.get_add_url(radio_show)

        response = self.get(add_url)
        assert "Add podcast" in response
        form = response.forms[1]
        assert form.action == add_url

        form['title'] = "Interview with a person"
        form['description'] = (
            response.context['form']
            .fields['description']
            .widget.format_value("<p>Description of this podcast.</p>")
        )
        form['sound_url'] = 'https://example.org/podcast1.ogg'
        form['is_sound_valid'] = '1'
        form['publish_date'] = '2022-01-01 12:00:00'
        response = form.submit(status=302)
        assert response['location'] == self.get_index_url(radio_show)
        assert escape("'Interview with a person' added") in response.follow()

        podcast = Podcast.objects.get(title="Interview with a person")
        assert podcast.radio_show == radio_show
        assert podcast.sound_url == 'https://example.org/podcast1.ogg'
        assert podcast.slug == 'interview-with-a-person'
        assert make_naive(podcast.publish_date) == datetime.datetime(
            2022, 1, 1, 12, 0
        )

    def test_edit(self):
        podcast = PodcastFactory()
        url = self.get_edit_url(podcast)

        form = self.get(url).forms[1]
        form['title'] = "Interview with a person"
        form['sound_url'] = 'https://example.org/interview1.ogg'
        form['is_sound_valid'] = True
        response = form.submit(status=302)
        assert response['location'] == self.get_index_url(podcast.radio_show)
        assert escape("'Interview with a person' updated") in response.follow()

        podcast.refresh_from_db()
        assert podcast.sound_url == 'https://example.org/interview1.ogg'

    def test_edit_invalid_sound_url(self):
        podcast = PodcastFactory()
        url = self.get_edit_url(podcast)

        form = self.get(url).forms[1]
        form['sound_url'] = 'http'
        form['is_sound_valid'] = '0'

        response = form.submit(status=200)
        errors = response.context['form'].errors['sound_url']
        assert len(errors) == 1
        assert errors[0] == "Enter a valid URL."

        form = response.forms[1]
        form['sound_url'] = 'http://localhost/some-file'
        form['is_sound_valid'] = '0'

        response = form.submit(status=200)
        errors = response.context['form'].errors[NON_FIELD_ERRORS]
        assert len(errors) == 1
        assert "Unable to retrieve an audio file" in errors[0]

    def test_delete(self):
        podcast = PodcastFactory()
        url = self.get_delete_url(podcast)

        delete_form = self.get(url, status=200).forms[1]
        assert delete_form.action == url

        delete_form.submit().follow(status=200)
        assert not Podcast.objects.filter(pk=podcast.pk).exists()


class TestPodcastAdminManagerViews(PodcastAdminViewsMixin, ViewTestMixin):
    @pytest.fixture(autouse=True)
    def setup_user(self, manager_user):
        self.user = manager_user

    def test_index(self, manager_radio_shows):
        radio_show = manager_radio_shows[2]
        podcast = PodcastFactory(radio_show=radio_show)

        html = self.get(self.get_index_url(radio_show), status=200).html
        assert html.find('a', href=self.get_add_url(radio_show)).text == (
            "Add a podcast"
        )
        rows = html.select('table.listing tbody > tr')
        assert len(rows) == 1
        assert rows[0].find('a', href=self.get_edit_url(podcast))

    def test_index_no_add_button(self, change_podcast_perm):
        radio_show = RadioShowFactory()
        podcast = PodcastFactory(radio_show=radio_show)
        self.user.user_permissions.add(change_podcast_perm)

        html = self.get(self.get_index_url(radio_show), status=200).html
        assert not html.find('a', href=self.get_add_url(radio_show))
        rows = html.select('table.listing tbody > tr')
        assert len(rows) == 1
        assert rows[0].find('a', href=self.get_edit_url(podcast))

    def test_index_unauthorized(self, manager_radio_shows):
        self.get(self.get_index_url(manager_radio_shows[3]), status=302)

    def test_add(self, manager_radio_shows):
        self.get(self.get_add_url(manager_radio_shows[2]), status=200)

    def test_add_unauthorized(self, manager_radio_shows):
        self.get(self.get_add_url(manager_radio_shows[3]), status=302)

    def test_edit(self, manager_radio_shows):
        podcast = PodcastFactory(radio_show=manager_radio_shows[2])

        self.get(self.get_edit_url(podcast), status=200)

    def test_edit_unauthorized(self, manager_radio_shows):
        podcast = PodcastFactory(radio_show=manager_radio_shows[3])

        self.get(self.get_edit_url(podcast), status=302)

    def test_delete(self, manager_radio_shows):
        podcast = PodcastFactory(radio_show=manager_radio_shows[2])

        self.get(self.get_delete_url(podcast), status=200)

    def test_delete_unauthorized(self, manager_radio_shows):
        podcast = PodcastFactory(radio_show=manager_radio_shows[1])

        self.get(self.get_delete_url(podcast), status=302)

    def test_default_error(self, manager_radio_shows):
        form = self.get(
            self.get_add_url(manager_radio_shows[2]), status=200
        ).form
        form['sound_url'] = 'https://no.lan/podcast.mp3'
        form['is_sound_valid'] = True
        response = form.submit()
        assert (
            response.context['message']
            == 'The podcast could not be created due to errors.'
        )

    def test_url_not_valid_error(self, manager_radio_shows):
        form = self.get(
            self.get_add_url(manager_radio_shows[2]), status=200
        ).form
        form['sound_url'] = 'https://no.lan/image.jpeg'
        response = form.submit()
        assert response.context['message'] == (
            "Unable to retrieve an audio file. Check that it is valid and "
            "supported by your web browser by opening it in a new tab."
        )

    def test_sound_file_not_valid_error(self, manager_radio_shows):
        form = self.get(
            self.get_add_url(manager_radio_shows[2]), status=200
        ).form
        form['sound_file'] = Upload('text_file.txt', b'data')
        response = form.submit()
        assert response.context['message'] == (
            'Unable to retrieve an audio file. Please verify the file format.'
        )

    def test_one_non_field_errors(self, manager_radio_shows):
        form = self.get(
            self.get_add_url(manager_radio_shows[2]), status=200
        ).form
        form['title'] = 'Title'
        response = form.submit()
        assert (
            response.context['message']
            == 'You must fill at least a sound file or a sound url'
        )


class TestPodcastChooser(AdminViewTestMixin):
    url = reverse('wagtail_webradio:podcast_chooser')
    results_url = reverse('wagtail_webradio:podcast_chooser_results')

    def test_chooser(self):
        PodcastFactory()
        PodcastFactory(title="A podcast", radio_show__title="A radio show")

        data = self.get(status=200).json
        assert data['step'] == 'choose'
        html = BeautifulSoup(data['html'], 'html.parser')
        html.select_one('h2').string == "Latest podcasts"
        rows = html.select('table.listing tbody > tr')
        assert len(rows) == 2
        cells = rows[0].select('td')
        assert cells[0].select_one('a').string == "A podcast"
        assert cells[1].string.strip() == "A radio show"

    def test_chooser_empty(self):
        data = self.get(status=200).json
        html = BeautifulSoup(data['html'], 'html.parser')
        assert not html.select('h2')
        assert not html.select('table.listing')
        assert html.select_one('.listing').text.strip() == (
            "You haven't added any podcasts."
        )

    def test_filtered_results(self):
        radio_show = RadioShowFactory()
        PodcastFactory(title="The foobar")
        PodcastFactory(radio_show=radio_show)
        PodcastFactory(title="Something else", radio_show=radio_show)

        params = {'q': "foo"}
        html = self.get(self.results_url, params, status=200).html
        html.select_one('h2').string.strip() == "There is 1 match"
        result_titles = html.select('table.listing a')
        assert len(result_titles) == 1
        assert result_titles[0].string == "The foobar"

        params = {'radio_show': radio_show.pk}
        html = self.get(self.results_url, params, status=200).html
        html.select_one('h2').string.strip() == "There are 2 matches"
        result_titles = html.select('table.listing a')
        assert len(result_titles) == 2
        assert result_titles[0].string == "Something else"

        params = {'q': "empty"}
        html = self.get(self.results_url, params, status=200).html
        assert not html.select('table.listing')
        assert html.text.strip() == "No podcasts match this filters."

        params = {'radio_show': 'invalid'}
        html = self.get(self.results_url, params, status=200).html
        html.select_one('h2').string.strip() == "Latest podcasts"
        result_titles = html.select('table.listing a')
        assert len(result_titles) == 3

    def test_choosen(self):
        podcast = PodcastFactory(title="A podcast")

        response = self.get(
            reverse('wagtail_webradio:podcast_chosen', args=(podcast.id,)),
            status=200,
        )
        assert response.json == {
            'step': 'chosen',
            'result': {
                'id': podcast.id,
                'title': "A podcast",
                'edit_link': reverse(
                    'wagtail_webradio:podcast_edit', args=(podcast.id,)
                ),
            },
        }


class TestGroupPermissionsView(AdminViewTestMixin):
    add_url = reverse('wagtailusers_groups:add')

    def get_edit_url(self, group=None):
        if group is None:
            group = self.group
        return reverse('wagtailusers_groups:edit', args=(group.pk,))

    @pytest.fixture(autouse=True)
    def setup_group(self):
        self.group = Group.objects.create(name='Radio show changers')

    def test_models_permissions(self):
        html = self.get(self.get_edit_url()).html
        assert html.select_one('label', string="Can add podcast")
        assert html.select_one('label', string="Can add radio show")

    def test_form_media(self):
        html = self.get(self.get_edit_url()).html
        assert html.find(
            'link',
            href=(
                '/static/wagtail_webradio/admin/css/'
                'radio_show_permissions.css'
            ),
        )

    def test_radio_show_permissions_order(
        self,
        change_radioshow_perm,
        add_podcast_perm,
        change_podcast_perm,
        delete_podcast_perm,
    ):
        GroupRadioShowPermission.objects.create(
            group=self.group,
            radio_show=RadioShowFactory(),
            permission=change_radioshow_perm,
        )

        response = self.get(self.get_edit_url())
        tbody = response.html.find(id='id_radio_show_permissions-FORMS')
        tbody_td = tbody.select('td')
        assert tbody_td[1].find('input').attrs['value'] == str(
            change_radioshow_perm.pk
        )
        assert tbody_td[2].find('input').attrs['value'] == str(
            add_podcast_perm.pk
        )
        assert tbody_td[3].find('input').attrs['value'] == str(
            change_podcast_perm.pk
        )
        assert tbody_td[4].find('input').attrs['value'] == str(
            delete_podcast_perm.pk
        )
        thead_th = tbody.find_parent('table').select('thead tr:last-child th')
        assert thead_th[1].string == "Edit"
        assert thead_th[2].attrs['title'] == "Add podcasts"
        assert thead_th[3].attrs['title'] == "Edit any podcast"
        assert thead_th[4].attrs['title'] == "Delete any podcast"

    def test_create_group_with_radio_show_permission(
        self, change_radioshow_perm
    ):
        radio_show = RadioShowFactory()

        response = self.get(self.add_url)
        form = response.forms[1]
        assert form.action == self.add_url

        # add permissions on the radio show
        add_inline_form_data(
            form,
            'radio_show_permissions',
            {
                'radio_show': str(radio_show.pk),
                'permissions': [str(change_radioshow_perm.pk)],
            },
        )
        form['name'] = "A new group"
        form.submit(status=302).follow()

        group = Group.objects.get(name="A new group")
        radio_show_permission = group.radio_show_permissions.get()
        assert radio_show_permission.radio_show == radio_show
        assert radio_show_permission.permission == change_radioshow_perm

        # check the radio show permissions in the edit form
        form = self.get(self.get_edit_url(group)).forms[1]
        assert form['radio_show_permissions-0-radio_show'].value == str(
            radio_show.pk
        )
        permissions_fields = form.fields['radio_show_permissions-0-permissions']
        assert permissions_fields[0].value == str(change_radioshow_perm.pk)
        assert permissions_fields[0].checked
        assert not permissions_fields[1].checked
        assert not permissions_fields[2].checked
        assert not permissions_fields[3].checked

    def test_delete_radio_show_permission(self, change_radioshow_perm):
        perm_to_delete = GroupRadioShowPermission.objects.create(
            group=self.group,
            radio_show=RadioShowFactory(),
            permission=change_radioshow_perm,
        )
        perm_to_keep = GroupRadioShowPermission.objects.create(
            group=self.group,
            radio_show=RadioShowFactory(),
            permission=change_radioshow_perm,
        )

        form = self.get(self.get_edit_url()).forms[1]
        assert form['radio_show_permissions-0-radio_show'].value == str(
            perm_to_delete.radio_show.pk
        )

        form['radio_show_permissions-0-DELETE'] = '1'
        form.submit(status=302).follow()

        assert not GroupRadioShowPermission.objects.filter(
            pk=perm_to_delete.pk
        ).exists()
        assert GroupRadioShowPermission.objects.filter(
            pk=perm_to_keep.pk
        ).exists()

    def test_multiple_permissions_for_the_same_radio_show(
        self, change_radioshow_perm, add_podcast_perm
    ):
        radio_show = RadioShowFactory()

        form = self.get(self.get_edit_url()).forms[1]

        add_inline_form_data(
            form,
            'radio_show_permissions',
            {
                'radio_show': '10000',
                'permissions': [str(change_radioshow_perm.pk)],
            },
        )
        add_inline_form_data(
            form,
            'radio_show_permissions',
            {
                'radio_show': str(radio_show.pk),
                'permissions': [str(add_podcast_perm.pk)],
            },
        )
        response = form.submit(status=200)
        permission_panel = response.context['permission_panels'][-1]
        # multiple records is tested only if there is no error
        assert not permission_panel.non_form_errors()
        assert 'radio_show' in permission_panel.errors[0]

        form = response.forms[1]
        form['radio_show_permissions-0-radio_show'] = str(radio_show.pk)
        response = form.submit(status=200)
        permission_panel = response.context['permission_panels'][-1]
        assert permission_panel.non_form_errors() == [
            "You cannot have multiple permission records for the same radio "
            "show."
        ]

    def test_unexpected_radio_show_permission(self):
        GroupRadioShowPermission.objects.create(
            group=self.group,
            radio_show=RadioShowFactory(),
            permission=Permission.objects.get(codename='delete_radioshow'),
        )

        form = self.get(self.get_edit_url()).forms[1]
        assert form['radio_show_permissions-TOTAL_FORMS'].value == '0'
