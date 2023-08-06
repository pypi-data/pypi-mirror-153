from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db.models import Q

from wagtail.core.permission_policies import BaseDjangoAuthPermissionPolicy

from . import RADIO_SHOW_ANY_PERMISSION_CODENAMES
from .models import GroupRadioShowPermission, Podcast, RadioShow


class RadioShowPermissionLookupMixin:
    def _get_permission_codenames(self, actions):
        """
        Get the permission codenames for the given actions on this model.
        """
        return ['%s_%s' % (action, self.model_name) for action in actions]

    def _get_permission_objects_for_actions(self, actions):
        """
        Get a queryset of the Permission objects for the given actions on this
        model.
        """
        return Permission.objects.filter(
            content_type=self._content_type,
            codename__in=self._get_permission_codenames(actions),
        )

    def _has_perms(self, user, actions, radio_show=None):
        """
        Return whether the given user has permission to perform any of the given
        actions using `user.has_perm` method - i.e. either through its group or
        user permissions, or implicitly through being a superuser - or through
        `GroupRadioShowPermission` records.
        If `radio_show` is specified, only `GroupRadioShowPermission` records
        that apply to that `RadioShow` object will be considered.
        """
        if not (user.is_active and user.is_authenticated):
            return False

        for action in actions:
            if user.has_perm(self._get_permission_name(action)):
                return True

        radio_show_permissions = GroupRadioShowPermission.objects.filter(
            group__user=user,
            permission__in=self._get_permission_objects_for_actions(actions),
        )

        if radio_show is not None:
            radio_show_permissions = radio_show_permissions.filter(
                radio_show=radio_show,
            )

        return radio_show_permissions.exists()

    def _get_radio_shows_with_perms(self, user, actions):
        """
        Return a queryset of radio shows on which this user has a
        `GroupRadioShowPermission` record for any of the given actions.
        """
        permissions = self._get_permission_objects_for_actions(actions)

        return RadioShow.objects.filter(
            group_permissions__group__in=user.groups.all(),
            group_permissions__permission__in=permissions,
        )

    def _get_users_with_perms_filter(self, actions, radio_show=None):
        """
        Return a filter expression that will filter a user queryset to those
        with any permissions corresponding to `actions`, via either its group
        permissions, user permissions, or implicitly through being a superuser,
        or `GroupRadioShowPermission`.
        If `radio_show` is specified, only `GroupRadioShowPermission` records
        that apply to that radio show will be considered.
        """
        permissions = self._get_permission_objects_for_actions(actions)

        filter_expr = (
            Q(is_superuser=True)
            | Q(user_permissions__in=permissions)
            | Q(groups__permissions__in=permissions)
        )

        groups = Group.objects.filter(
            radio_show_permissions__permission__in=permissions
        )

        if radio_show is not None:
            groups = groups.filter(
                radio_show_permissions__radio_show=radio_show
            )

        return Q(is_active=True) & (filter_expr | Q(groups__in=groups))

    def _get_users_with_perms(self, actions, radio_show=None):
        """
        Return a queryset of users with any permissions corresponding to
        `actions`, via either its group permissions, user permissions, or
        implicitly through being a superuser, or `GroupRadioShowPermission`.
        If `radio_show` is specified, only `GroupRadioShowPermission` records
        that apply to that radio show will be considered.
        """
        return (
            get_user_model()
            .objects.filter(
                self._get_users_with_perms_filter(
                    actions, radio_show=radio_show
                )
            )
            .distinct()
        )

    def radio_shows_user_has_any_permission_for(self, user, actions):
        """
        Return a queryset of all radio shows on which the given user has
        permission to perform any of the given actions.
        """
        if not (user.is_active and user.is_authenticated):
            return RadioShow.objects.none()

        for action in actions:
            if user.has_perm(self._get_permission_name(action)):
                return RadioShow.objects.all()

        return self._get_radio_shows_with_perms(user, actions)

    def radio_shows_user_has_permission_for(self, user, action):
        """
        Return a queryset of all radio shows on which the given user has
        permission to perform the given action.
        """
        return self.radio_shows_user_has_any_permission_for(user, [action])


class RadioShowPermissionPolicy(
    RadioShowPermissionLookupMixin, BaseDjangoAuthPermissionPolicy
):
    def __init__(self, model):
        super().__init__(model)

        if model != RadioShow:
            raise ImproperlyConfigured(
                "%s is not RadioShow model." % self.model
            )  # pragma: no cover

    def user_has_permission(self, user, action):
        return self._has_perms(user, [action])

    def user_has_any_permission(self, user, actions):
        return self._has_perms(user, actions)

    def users_with_any_permission(self, actions):
        return self._get_users_with_perms(actions)

    def user_has_permission_for_instance(self, user, action, instance):
        return self._has_perms(user, [action], radio_show=instance)

    def user_has_any_permission_for_instance(self, user, actions, instance):
        return self._has_perms(user, actions, radio_show=instance)

    def instances_user_has_any_permission_for(self, user, actions=None):
        """
        Return a queryset of all instances of `RadioShow` for which the given
        user has permission to perform any of the given actions.
        If `actions` is not specified, permission lookup will be enlarged to
        consider related models too for any relevant actions - e.g. add a
        podcast in a radio show.
        """
        if actions is not None:
            return self.radio_shows_user_has_any_permission_for(user, actions)

        for codename in RADIO_SHOW_ANY_PERMISSION_CODENAMES:
            if user.has_perm('%s.%s' % (self.app_label, codename)):
                return RadioShow.objects.all()

        return RadioShow.objects.filter(
            group_permissions__group__in=user.groups.all()
        ).distinct()

    def instances_user_has_permission_for(self, user, action):
        return self.radio_shows_user_has_permission_for(user, action)

    def users_with_any_permission_for_instance(self, actions, instance):
        return self._get_users_with_perms(actions, radio_show=instance)


class RadioShowRelatedPermissionPolicy(
    RadioShowPermissionLookupMixin, BaseDjangoAuthPermissionPolicy
):
    """
    A permission policy for objects that are linked to a RadioShow through a
    field named `radio_show_field_name`. Permissions may be defined generally
    for the model itself or granted from a `GroupRadioShowPermission` record.
    """

    def __init__(self, model, radio_show_field_name='radio_show'):
        super().__init__(model)

        self.radio_show_field_name = radio_show_field_name

        try:
            self.model._meta.get_field(self.radio_show_field_name)
        except FieldDoesNotExist:  # pragma: no cover
            raise ImproperlyConfigured(
                "%s has no field named '%s'. To use this model with "
                "RadioShowRelatedPermissionPolicy, you must specify a valid "
                "field name as radio_show_field_name."
                % (self.model, self.radio_show_field_name)
            )

    def _get_radio_show_from_instance(self, instance):
        return getattr(instance, self.radio_show_field_name)

    def user_has_permission(self, user, action):
        return self._has_perms(user, [action])

    def user_has_any_permission(self, user, actions):
        return self._has_perms(user, actions)

    def users_with_any_permission(self, actions):
        return self._get_users_with_perms(actions)

    def user_has_permission_for_instance(self, user, action, instance):
        return self._has_perms(
            user,
            [action],
            radio_show=self._get_radio_show_from_instance(instance),
        )

    def user_has_any_permission_for_instance(self, user, actions, instance):
        return self._has_perms(
            user,
            actions,
            radio_show=self._get_radio_show_from_instance(instance),
        )

    def instances_user_has_any_permission_for(self, user, actions):
        """
        Return a queryset of all instances of this model for which the given
        user has permission to perform any of the given actions, either through
        its group or user permissions, implicitly through being a superuser, or
        through related `GroupRadioShowPermission` records.
        """
        field_lookup = '%s__in' % self.radio_show_field_name
        radio_shows = self.radio_shows_user_has_any_permission_for(
            user, actions
        )
        return self.model.objects.filter(**{field_lookup: radio_shows})

    def users_with_any_permission_for_instance(self, actions, instance):
        return self._get_users_with_perms(
            actions,
            radio_show=self._get_radio_show_from_instance(instance),
        )

    def user_has_permission_for_radio_show(self, user, action, radio_show):
        """
        Return whether the given user has permission to perform the given action
        on the given `RadioShow` instance.
        """
        return self._has_perms(user, [action], radio_show=radio_show)

    def user_has_any_permission_for_radio_show(self, user, actions, radio_show):
        """
        Return whether the given user has permission to perform any of the given
        actions on the given `RadioShow` instance.
        """
        return self._has_perms(user, actions, radio_show=radio_show)


podcast_permission_policy = RadioShowRelatedPermissionPolicy(Podcast)
radio_show_permission_policy = RadioShowPermissionPolicy(RadioShow)
