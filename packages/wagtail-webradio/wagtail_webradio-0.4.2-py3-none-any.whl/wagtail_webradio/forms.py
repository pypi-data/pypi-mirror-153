from itertools import groupby

from django import forms
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import transaction
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import Media
from django.template.loader import render_to_string
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, ObjectList
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.images.edit_handlers import ImageChooserPanel

from . import (
    GROUP_RADIO_SHOW_PERMISSION_CODENAMES,
    GROUP_RADIO_SHOW_PERMISSION_TYPES,
)
from .models import GroupRadioShowPermission, RadioShow


def get_podcast_excluded_fields():
    sound_file = getattr(settings, 'WEBRADIO_SOUND_FILE', True)
    return ('sound_file',) if not sound_file else ()


class PodcastAdminForm(WagtailAdminModelForm):
    """
    Form used for creating and editing a Podcast in the admin.

    The `sound_url` value or the `sound_file` will be validated on client side
    by loading it as an Audio object. This will trigger the `is_sound_valid`
    field and set the `duration` field if the audio could be loaded.
    """

    is_sound_valid = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )

    class Media:
        js = ('wagtail_webradio/admin/js/podcast-form.js',)

    class Meta:
        exclude = get_podcast_excluded_fields()

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get('sound_url')
            and not cleaned_data.get('is_sound_valid')
            and 'sound_url' not in self.errors
        ):
            self.add_error(
                NON_FIELD_ERRORS,
                ValidationError(
                    _(
                        "Unable to retrieve an audio file. Check "
                        "that it is valid and supported by your web browser by "
                        "opening it in a new tab."
                    )
                ),
            )
        if (
            cleaned_data.get('sound_file')
            and not cleaned_data.get('is_sound_valid')
            and 'sound_file' not in self.errors
        ):
            self.add_error(
                NON_FIELD_ERRORS,
                ValidationError(
                    _(
                        "Unable to retrieve an audio file. "
                        "Please verify the file format."
                    )
                ),
            )


class PodcastChooserSearchForm(forms.Form):
    """
    Search form used for the Podcast chooser widget.
    """

    q = forms.CharField(
        label=_("Search term"),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _("Search")}),
    )
    radio_show = forms.ModelChoiceField(
        label=_("Radio show"),
        required=False,
        queryset=RadioShow.objects.all(),
        empty_label=_("All radio shows"),
    )

    def filter(self, queryset):
        """Filter the given queryset with the form data."""
        if self.cleaned_data.get('radio_show', None):
            queryset = queryset.filter(
                radio_show_id=self.cleaned_data['radio_show']
            )

        if self.cleaned_data.get('q', None):
            # Filtering on the title will be faster than using search backend
            queryset = queryset.filter(title__icontains=self.cleaned_data['q'])

        return queryset


class RadioShowPermissionChoiceIterator(ModelChoiceIterator):
    """
    Iterate over permission checkboxes in the same order than what is displayed
    in the header - i.e. the order of ``GROUP_RADIO_SHOW_PERMISSION_TYPES``.
    """

    def __iter__(self):
        assert self.field.empty_label is None, "empty_label should be None"

        indexed_permissions = {obj.codename: obj for obj in self.queryset}

        for codename in GROUP_RADIO_SHOW_PERMISSION_CODENAMES:
            yield self.choice(indexed_permissions.pop(codename))

        assert not indexed_permissions, "Unexpected permission objects left"


class RadioShowPermissionMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Allow the custom labels from ``GROUP_RADIO_SHOW_PERMISSION_TYPES`` to be
    applied to permission checkboxes for the ``RadioShowPermissionsForm``.
    """

    iterator = RadioShowPermissionChoiceIterator

    def label_from_instance(self, obj):
        for codename, label, help_text in GROUP_RADIO_SHOW_PERMISSION_TYPES:
            if codename == obj.codename:
                return help_text

        raise AssertionError("Unexpected permission object '%s'" % obj)


class RadioShowPermissionsForm(forms.Form):
    """
    Define the permissions that are assigned to an entity - i.e. group or
    user - for a specific radio show.
    """

    radio_show = forms.ModelChoiceField(
        label=_("Radio show"),
        empty_label=None,
        queryset=RadioShow.objects.all().prefetch_related('group_permissions'),
    )
    permissions = RadioShowPermissionMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=(
            Permission.objects.filter(
                content_type__app_label=RadioShow._meta.app_label,
                codename__in=GROUP_RADIO_SHOW_PERMISSION_CODENAMES,
            ).select_related('content_type')
        ),
    )


class BaseGroupRadioShowPermissionFormSet(forms.BaseFormSet):
    """
    The base formset class for managing ``GroupRadioShowPermission``.

    This class and related ones are adapted from what is produced by
    `wagtail.admin.forms.collections.collection_member_permission_formset_factory`.
    """

    permission_queryset = Permission.objects.filter(
        content_type__app_label=RadioShow._meta.app_label,
        codename__in=GROUP_RADIO_SHOW_PERMISSION_CODENAMES,
    )
    permission_types = GROUP_RADIO_SHOW_PERMISSION_TYPES

    def __init__(
        self,
        data=None,
        files=None,
        instance=None,
        prefix='radio_show_permissions',
    ):
        initial_data = []

        if instance is not None:
            # add the group's existing radio show permissions to initial data
            for radio_show, radio_show_permissions in groupby(
                instance.radio_show_permissions.filter(
                    permission__in=self.permission_queryset
                )
                .select_related('permission__content_type', 'radio_show')
                .order_by('radio_show'),
                lambda obj: obj.radio_show,
            ):
                initial_data.append(
                    {
                        'radio_show': radio_show,
                        'permissions': [
                            obj.permission for obj in radio_show_permissions
                        ],
                    }
                )
        else:
            instance = Group()
        self.instance = instance

        super().__init__(data, files, initial=initial_data, prefix=prefix)

        for form in self.forms:
            form.fields['DELETE'].widget = forms.HiddenInput()

    @property
    def empty_form(self):
        empty_form = super().empty_form
        empty_form.fields['DELETE'].widget = forms.HiddenInput()
        return empty_form

    def clean(self):
        """Checks that no two forms refer to the same radio show object."""
        if any(self.errors):
            return

        radio_shows = [
            form.cleaned_data['radio_show']
            for form in self.forms
            # need to check for presence of 'radio_show' in cleaned_data,
            # because a completely blank form passes validation
            if form not in self.deleted_forms
            and 'radio_show' in form.cleaned_data
        ]
        if len(set(radio_shows)) != len(radio_shows):
            raise forms.ValidationError(
                gettext(
                    "You cannot have multiple permission records for the same "
                    "radio show."
                )
            )

    @transaction.atomic
    def save(self):
        assert self.instance.pk is not None, (
            "Cannot save a GroupRadioShowPermissionFormSet for an unsaved "
            "group instance"
        )

        forms_to_save = [
            form
            for form in self.forms
            if form not in self.deleted_forms
            and 'radio_show' in form.cleaned_data
        ]

        # get a set of (radio_show, permission) for all ticked permissions
        permission_records = {
            (form.cleaned_data['radio_show'], permission)
            for form in forms_to_save
            for permission in form.cleaned_data['permissions']
        }

        # fetch the group's existing radio show permission records, and from
        # that, build a list of records to be created / deleted
        permission_ids_to_delete = []
        permission_records_to_keep = set()
        for gp in self.instance.radio_show_permissions.filter(
            permission__in=self.permission_queryset
        ):
            if (gp.radio_show, gp.permission) in permission_records:
                permission_records_to_keep.add((gp.radio_show, gp.permission))
            else:
                permission_ids_to_delete.append(gp.id)

        self.instance.radio_show_permissions.filter(
            id__in=permission_ids_to_delete
        ).delete()

        GroupRadioShowPermission.objects.bulk_create(
            [
                GroupRadioShowPermission(
                    group=self.instance,
                    radio_show=radio_show,
                    permission=permission,
                )
                for (radio_show, permission) in (
                    permission_records - permission_records_to_keep
                )
            ]
        )

    def as_admin_panel(self):
        return render_to_string(
            (
                'wagtail_webradio/permissions/includes/'
                'radio_show_permissions_formset.html'
            ),
            {'formset': self},
        )

    @property
    def media(self):
        return (
            Media(
                css={
                    'screen': [
                        'wagtail_webradio/admin/css/radio_show_permissions.css'
                    ]
                }
            )
            + super().media
        )


GroupRadioShowPermissionFormSet = forms.formset_factory(
    RadioShowPermissionsForm,
    formset=BaseGroupRadioShowPermissionFormSet,
    extra=0,
    can_delete=True,
)

# EDIT HANDLERS
# ------------------------------------------------------------------------------

radio_show_edit_handler = ObjectList(
    [
        FieldPanel('title', classname='title full'),
        MultiFieldPanel(
            [
                FieldPanel('description'),
                ImageChooserPanel('picture'),
            ],
            heading=_("Description"),
        ),
        MultiFieldPanel(
            [
                FieldPanel('contact_phone'),
                FieldPanel('contact_email'),
            ],
            heading=_("Contact"),
        ),
    ],
)

podcast_edit_handler = ObjectList(
    [
        FieldPanel('title', classname='title full'),
        MultiFieldPanel(
            [
                FieldPanel('description'),
                ImageChooserPanel('picture'),
                FieldPanel('tags'),
            ],
            heading=_("Description"),
        ),
        MultiFieldPanel(
            [
                FieldPanel('sound_file'),
                FieldPanel('sound_url'),
                FieldPanel(
                    'duration',
                    widget=forms.TimeInput(
                        attrs={'title': gettext("The format must be HH:MM:SS")},
                        format='%H:%M:%S',
                    ),
                ),
            ],
            heading=_("Media"),
        ),
        MultiFieldPanel(
            [
                FieldPanel('publish_date', heading=_("Date")),
            ],
            heading=_("Publishing"),
        ),
    ],
    base_form_class=PodcastAdminForm,
)
