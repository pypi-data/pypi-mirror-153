from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.db import transaction

import pytest

from wagtail_webradio.models import GroupRadioShowPermission
from wagtail_webradio.permissions import (
    podcast_permission_policy,
    radio_show_permission_policy,
)

from .factories import PodcastFactory, RadioShowFactory

User = get_user_model()


class PermissionPolicyMixin:
    @pytest.fixture(autouse=True, scope='class')
    def setup_class_objects(self, django_db_setup, django_db_blocker, request):
        with django_db_blocker.unblock():
            with transaction.atomic():
                sid = transaction.savepoint()
                request.cls.create_objects()

                yield  # wait for the end of the class' tests

                transaction.savepoint_rollback(sid)

    @classmethod
    def create_objects(cls):
        cls.main_show = RadioShowFactory(title="Main show")
        cls.other_show = RadioShowFactory(title="Other show")

        # Permissions

        add_radioshow_permission = Permission.objects.get(
            codename='add_radioshow',
        )
        change_radioshow_permission = Permission.objects.get(
            codename='change_radioshow',
        )
        add_podcast_permission = Permission.objects.get(
            codename='add_podcast',
        )
        change_podcast_permission = Permission.objects.get(
            codename='change_podcast',
        )
        delete_podcast_permission = Permission.objects.get(
            codename='delete_podcast',
        )

        # Groups

        managers_group = Group.objects.create(name="Managers")
        managers_group.permissions.add(
            add_radioshow_permission,
            change_radioshow_permission,
            add_podcast_permission,
            change_podcast_permission,
            delete_podcast_permission,
        )

        main_managers_group = Group.objects.create(name="Main managers")
        for perm in (
            change_radioshow_permission,
            add_podcast_permission,
            change_podcast_permission,
        ):
            GroupRadioShowPermission.objects.create(
                group=main_managers_group,
                radio_show=cls.main_show,
                permission=perm,
            )

        podcasters_group = Group.objects.create(name="Podcasters")
        podcasters_group.permissions.add(
            add_podcast_permission,
            change_podcast_permission,
        )

        main_podcasters_group = Group.objects.create(name="Main podcasters")
        for perm in (
            add_podcast_permission,
            change_podcast_permission,
        ):
            GroupRadioShowPermission.objects.create(
                group=main_podcasters_group,
                radio_show=cls.main_show,
                permission=perm,
            )

        # Users

        cls.superuser = User.objects.create_superuser(
            'superuser', 'superuser@example.org', 'password'
        )

        cls.inactive_superuser = User.objects.create_superuser(
            'inactivesuperuser', 'inactivesuperuser@example.org', 'password'
        )
        cls.inactive_superuser.is_active = False
        cls.inactive_superuser.save()

        cls.manager = User.objects.create_user(
            'manager', 'manager@example.org', 'password'
        )
        cls.manager.groups.add(managers_group)

        cls.main_manager = User.objects.create_user(
            'mainmanager', 'mainmanager@example.org', 'password'
        )
        cls.main_manager.groups.add(main_managers_group)

        cls.podcaster = User.objects.create_user(
            'podcaster', 'podcaster@example.org', 'password'
        )
        cls.podcaster.groups.add(podcasters_group)

        cls.main_podcaster = User.objects.create_user(
            'mainpodcaster', 'mainpodcaster@example.org', 'password'
        )
        cls.main_podcaster.groups.add(main_podcasters_group)

        cls.special_podcaster = User.objects.create_user(
            'specialpodcaster', 'specialpodcaster@example.org', 'password'
        )
        cls.special_podcaster.groups.add(main_podcasters_group)
        cls.special_podcaster.user_permissions.add(delete_podcast_permission)

        cls.useless_user = User.objects.create_user(
            'uselessuser', 'uselessuser@example.org', 'password'
        )

        cls.anonymous_user = AnonymousUser()


class TestRadioShowPermissionPolicy(PermissionPolicyMixin):
    policy = radio_show_permission_policy

    @pytest.mark.parametrize(
        'user_attr, perms',
        [
            ('superuser', (True, True, True, True)),
            ('inactive_superuser', (False, False, False, False)),
            ('manager', (True, True, False, False)),
            ('main_manager', (False, True, False, False)),
            ('podcaster', (False, False, False, False)),
            ('main_podcaster', (False, False, False, False)),
            ('useless_user', (False, False, False, False)),
            ('anonymous_user', (False, False, False, False)),
        ],
    )
    def test_user_has_permission(self, user_attr, perms):
        user = getattr(self, user_attr)
        can_add, can_change, can_delete, can_foobar = perms
        assert self.policy.user_has_permission(user, 'add') is can_add
        assert self.policy.user_has_permission(user, 'change') is can_change
        assert self.policy.user_has_permission(user, 'delete') is can_delete
        assert self.policy.user_has_permission(user, 'foobar') is can_foobar

    @pytest.mark.parametrize(
        'user_attr, result',
        [
            ('superuser', True),
            ('inactive_superuser', False),
            ('manager', True),
            ('main_manager', True),
            ('podcaster', False),
            ('main_podcaster', False),
            ('useless_user', False),
            ('anonymous_user', False),
        ],
    )
    def test_user_has_any_permission(self, user_attr, result):
        assert (
            self.policy.user_has_any_permission(
                getattr(self, user_attr), ['add', 'change']
            )
            is result
        )

    def test_users_with_any_permission(self):
        assert set(
            self.policy.users_with_any_permission(['add', 'change'])
        ) == {self.superuser, self.manager, self.main_manager}

    def test_users_with_permission(self):
        assert set(self.policy.users_with_permission('add')) == {
            self.superuser,
            self.manager,
        }

        assert set(self.policy.users_with_permission('foobar')) == {
            self.superuser
        }

    @pytest.mark.parametrize(
        'user_attr, perms',
        [
            ('superuser', (True, True, True, True)),
            ('inactive_superuser', (False, False, False, False)),
            ('manager', (True, True, False, False)),
            ('main_manager', (False, True, False, False)),
            ('podcaster', (False, False, False, False)),
            ('main_podcaster', (False, False, False, False)),
            ('useless_user', (False, False, False, False)),
            ('anonymous_user', (False, False, False, False)),
        ],
    )
    def test_user_has_permission_for_instance__main(self, user_attr, perms):
        user = getattr(self, user_attr)
        can_add, can_change, can_delete, can_foobar = perms
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'add', self.main_show
            )
            is can_add
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'change', self.main_show
            )
            is can_change
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'delete', self.main_show
            )
            is can_delete
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'foobar', self.main_show
            )
            is can_foobar
        )

    @pytest.mark.parametrize(
        'user_attr, perms',
        [
            ('superuser', (True, True, True, True)),
            ('inactive_superuser', (False, False, False, False)),
            ('manager', (True, True, False, False)),
            ('main_manager', (False, False, False, False)),
            ('podcaster', (False, False, False, False)),
            ('main_podcaster', (False, False, False, False)),
            ('useless_user', (False, False, False, False)),
            ('anonymous_user', (False, False, False, False)),
        ],
    )
    def test_user_has_permission_for_instance__other(self, user_attr, perms):
        user = getattr(self, user_attr)
        can_add, can_change, can_delete, can_foobar = perms
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'add', self.other_show
            )
            is can_add
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'change', self.other_show
            )
            is can_change
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'delete', self.other_show
            )
            is can_delete
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'foobar', self.other_show
            )
            is can_foobar
        )

    def test_user_has_any_permission_for_instance(self):
        assert self.policy.user_has_any_permission_for_instance(
            self.main_manager, ['add', 'change'], self.main_show
        )
        assert not self.policy.user_has_any_permission_for_instance(
            self.main_manager, ['add', 'change'], self.other_show
        )

        assert not self.policy.user_has_any_permission_for_instance(
            self.main_podcaster, ['add', 'change'], self.main_show
        )

        assert not self.policy.user_has_any_permission_for_instance(
            self.anonymous_user, ['add', 'change'], self.main_show
        )

    def test_instances_user_has_permission_for(self):
        assert set(
            self.policy.instances_user_has_permission_for(
                self.superuser, 'change'
            )
        ) == {self.main_show, self.other_show}

        assert not self.policy.instances_user_has_permission_for(
            self.inactive_superuser, 'change'
        )

        assert set(
            self.policy.instances_user_has_permission_for(
                self.manager, 'change'
            )
        ) == {self.main_show, self.other_show}

        assert set(
            self.policy.instances_user_has_permission_for(
                self.main_manager, 'change'
            )
        ) == {self.main_show}

        assert not self.policy.instances_user_has_permission_for(
            self.podcaster, 'change'
        )

        assert not self.policy.instances_user_has_permission_for(
            self.useless_user, 'change'
        )

        assert not self.policy.instances_user_has_permission_for(
            self.anonymous_user, 'change'
        )

    def test_instances_user_has_any_permission_for(self):
        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.superuser, ['add', 'change']
            )
        ) == {self.main_show, self.other_show}

        assert not self.policy.instances_user_has_any_permission_for(
            self.inactive_superuser, ['add', 'change']
        )

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.manager, ['add', 'change']
            )
        ) == {self.main_show, self.other_show}

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.main_manager, ['add', 'change']
            )
        ) == {self.main_show}

        assert not self.policy.instances_user_has_any_permission_for(
            self.podcaster, ['add', 'change']
        )

        assert not self.policy.instances_user_has_any_permission_for(
            self.main_podcaster, ['add', 'change']
        )

        assert not self.policy.instances_user_has_any_permission_for(
            self.useless_user, ['add', 'change']
        )

        assert not self.policy.instances_user_has_any_permission_for(
            self.anonymous_user, ['add', 'change']
        )

    def test_instances_user_has_any_permission_for_all(self):
        assert set(
            self.policy.instances_user_has_any_permission_for(self.superuser)
        ) == {self.main_show, self.other_show}

        assert not self.policy.instances_user_has_any_permission_for(
            self.inactive_superuser
        )

        assert set(
            self.policy.instances_user_has_any_permission_for(self.manager)
        ) == {self.main_show, self.other_show}

        assert set(
            self.policy.instances_user_has_any_permission_for(self.main_manager)
        ) == {self.main_show}

        assert set(
            self.policy.instances_user_has_any_permission_for(self.podcaster)
        ) == {self.main_show, self.other_show}

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.main_podcaster
            )
        ) == {self.main_show}

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.special_podcaster
            )
        ) == {self.main_show, self.other_show}

        assert not self.policy.instances_user_has_any_permission_for(
            self.useless_user
        )

        assert not self.policy.instances_user_has_any_permission_for(
            self.anonymous_user
        )

    def test_users_with_permission_for_instance(self):
        assert set(
            self.policy.users_with_permission_for_instance(
                'change', self.main_show
            )
        ) == {self.superuser, self.manager, self.main_manager}

        assert set(
            self.policy.users_with_permission_for_instance(
                'change', self.other_show
            )
        ) == {self.superuser, self.manager}

    def test_users_with_any_permission_for_instance(self):
        assert set(
            self.policy.users_with_any_permission_for_instance(
                ['add', 'change'], self.main_show
            )
        ) == {self.superuser, self.manager, self.main_manager}

        assert set(
            self.policy.users_with_any_permission_for_instance(
                ['add', 'change'], self.other_show
            )
        ) == {self.superuser, self.manager}

        assert set(
            self.policy.users_with_any_permission_for_instance(
                ['delete', 'foobar'], self.other_show
            )
        ) == {self.superuser}


class TestPodcastPermissionPolicy(PermissionPolicyMixin):
    policy = podcast_permission_policy

    @classmethod
    def create_objects(cls):
        super().create_objects()

        cls.main_podcast = PodcastFactory(radio_show=cls.main_show)
        cls.other_podcast = PodcastFactory(radio_show=cls.other_show)

    @pytest.mark.parametrize(
        'user_attr, perms',
        [
            ('superuser', (True, True, True, True)),
            ('inactive_superuser', (False, False, False, False)),
            ('manager', (True, True, True, False)),
            ('main_manager', (True, True, False, False)),
            ('podcaster', (True, True, False, False)),
            ('main_podcaster', (True, True, False, False)),
            ('special_podcaster', (True, True, True, False)),
            ('useless_user', (False, False, False, False)),
            ('anonymous_user', (False, False, False, False)),
        ],
    )
    def test_user_has_permission(self, user_attr, perms):
        user = getattr(self, user_attr)
        can_add, can_change, can_delete, can_foobar = perms
        assert self.policy.user_has_permission(user, 'add') is can_add
        assert self.policy.user_has_permission(user, 'change') is can_change
        assert self.policy.user_has_permission(user, 'delete') is can_delete
        assert self.policy.user_has_permission(user, 'foobar') is can_foobar

    @pytest.mark.parametrize(
        'user_attr, result',
        [
            ('superuser', True),
            ('inactive_superuser', False),
            ('manager', True),
            ('main_manager', True),
            ('podcaster', True),
            ('main_podcaster', True),
            ('special_podcaster', True),
            ('useless_user', False),
            ('anonymous_user', False),
        ],
    )
    def test_user_has_any_permission(self, user_attr, result):
        assert (
            self.policy.user_has_any_permission(
                getattr(self, user_attr), ['add', 'change']
            )
            is result
        )

    def test_users_with_any_permission(self):
        assert set(
            self.policy.users_with_any_permission(['add', 'change'])
        ) == {
            self.superuser,
            self.manager,
            self.main_manager,
            self.podcaster,
            self.main_podcaster,
            self.special_podcaster,
        }

    def test_users_with_permission(self):
        assert set(self.policy.users_with_permission('add')) == {
            self.superuser,
            self.manager,
            self.main_manager,
            self.podcaster,
            self.main_podcaster,
            self.special_podcaster,
        }

        assert set(self.policy.users_with_permission('foobar')) == {
            self.superuser
        }

    @pytest.mark.parametrize(
        'user_attr, perms',
        [
            ('superuser', (True, True, True, True)),
            ('inactive_superuser', (False, False, False, False)),
            ('manager', (True, True, True, False)),
            ('main_manager', (True, True, False, False)),
            ('podcaster', (True, True, False, False)),
            ('main_podcaster', (True, True, False, False)),
            ('special_podcaster', (True, True, True, False)),
            ('useless_user', (False, False, False, False)),
            ('anonymous_user', (False, False, False, False)),
        ],
    )
    def test_user_has_permission_for_instance__main(self, user_attr, perms):
        user = getattr(self, user_attr)
        can_add, can_change, can_delete, can_foobar = perms
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'add', self.main_podcast
            )
            is can_add
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'change', self.main_podcast
            )
            is can_change
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'delete', self.main_podcast
            )
            is can_delete
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'foobar', self.main_podcast
            )
            is can_foobar
        )

    @pytest.mark.parametrize(
        'user_attr, perms',
        [
            ('superuser', (True, True, True, True)),
            ('inactive_superuser', (False, False, False, False)),
            ('manager', (True, True, True, False)),
            ('main_manager', (False, False, False, False)),
            ('podcaster', (True, True, False, False)),
            ('main_podcaster', (False, False, False, False)),
            ('special_podcaster', (False, False, True, False)),
            ('useless_user', (False, False, False, False)),
            ('anonymous_user', (False, False, False, False)),
        ],
    )
    def test_user_has_permission_for_instance__other(self, user_attr, perms):
        user = getattr(self, user_attr)
        can_add, can_change, can_delete, can_foobar = perms
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'add', self.other_podcast
            )
            is can_add
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'change', self.other_podcast
            )
            is can_change
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'delete', self.other_podcast
            )
            is can_delete
        )
        assert (
            self.policy.user_has_permission_for_instance(
                user, 'foobar', self.other_podcast
            )
            is can_foobar
        )

    def test_user_has_any_permission_for_instance(self):
        assert self.policy.user_has_any_permission_for_instance(
            self.main_manager, ['add', 'change'], self.main_podcast
        )
        assert not self.policy.user_has_any_permission_for_instance(
            self.main_manager, ['add', 'change'], self.other_podcast
        )

        assert self.policy.user_has_any_permission_for_instance(
            self.main_podcaster, ['add', 'change'], self.main_podcast
        )
        assert not self.policy.user_has_any_permission_for_instance(
            self.main_podcaster, ['add', 'change'], self.other_podcast
        )

        assert self.policy.user_has_any_permission_for_instance(
            self.special_podcaster, ['add', 'delete'], self.main_podcast
        )
        assert self.policy.user_has_any_permission_for_instance(
            self.special_podcaster, ['add', 'delete'], self.other_podcast
        )

        assert not self.policy.user_has_any_permission_for_instance(
            self.anonymous_user, ['add', 'change'], self.main_podcast
        )

    def test_instances_user_has_permission_for(self):
        assert set(
            self.policy.instances_user_has_permission_for(
                self.superuser, 'change'
            )
        ) == {self.main_podcast, self.other_podcast}

        assert not self.policy.instances_user_has_permission_for(
            self.inactive_superuser, 'change'
        )

        assert set(
            self.policy.instances_user_has_permission_for(
                self.manager, 'change'
            )
        ) == {self.main_podcast, self.other_podcast}

        assert set(
            self.policy.instances_user_has_permission_for(
                self.main_manager, 'change'
            )
        ) == {self.main_podcast}

        assert set(
            self.policy.instances_user_has_permission_for(
                self.podcaster, 'change'
            )
        ) == {self.main_podcast, self.other_podcast}

        assert set(
            self.policy.instances_user_has_permission_for(
                self.main_podcaster, 'change'
            )
        ) == {self.main_podcast}

        assert set(
            self.policy.instances_user_has_permission_for(
                self.special_podcaster, 'change'
            )
        ) == {self.main_podcast}
        assert set(
            self.policy.instances_user_has_permission_for(
                self.special_podcaster, 'delete'
            )
        ) == {self.main_podcast, self.other_podcast}

        assert not self.policy.instances_user_has_permission_for(
            self.useless_user, 'change'
        )

        assert not self.policy.instances_user_has_permission_for(
            self.anonymous_user, 'change'
        )

    def test_instances_user_has_any_permission_for(self):
        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.superuser, ['add', 'change']
            )
        ) == {self.main_podcast, self.other_podcast}

        assert not self.policy.instances_user_has_any_permission_for(
            self.inactive_superuser, ['add', 'change']
        )

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.manager, ['add', 'change']
            )
        ) == {self.main_podcast, self.other_podcast}

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.main_manager, ['add', 'change']
            )
        ) == {self.main_podcast}

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.podcaster, ['add', 'change']
            )
        ) == {self.main_podcast, self.other_podcast}

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.main_podcaster, ['add', 'change']
            )
        ) == {self.main_podcast}

        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.special_podcaster, ['add', 'change']
            )
        ) == {self.main_podcast}
        assert set(
            self.policy.instances_user_has_any_permission_for(
                self.special_podcaster, ['add', 'delete']
            )
        ) == {self.main_podcast, self.other_podcast}

        assert not self.policy.instances_user_has_any_permission_for(
            self.useless_user, ['add', 'change']
        )

        assert not self.policy.instances_user_has_any_permission_for(
            self.anonymous_user, ['add', 'change']
        )

    def test_users_with_permission_for_instance(self):
        assert set(
            self.policy.users_with_permission_for_instance(
                'change', self.main_podcast
            )
        ) == {
            self.superuser,
            self.manager,
            self.main_manager,
            self.podcaster,
            self.main_podcaster,
            self.special_podcaster,
        }

        assert set(
            self.policy.users_with_permission_for_instance(
                'delete', self.other_podcast
            )
        ) == {
            self.superuser,
            self.manager,
            self.special_podcaster,
        }

    def test_users_with_any_permission_for_instance(self):
        assert set(
            self.policy.users_with_any_permission_for_instance(
                ['add', 'change'], self.main_podcast
            )
        ) == {
            self.superuser,
            self.manager,
            self.main_manager,
            self.podcaster,
            self.main_podcaster,
            self.special_podcaster,
        }

        assert set(
            self.policy.users_with_any_permission_for_instance(
                ['add', 'delete'], self.other_podcast
            )
        ) == {
            self.superuser,
            self.manager,
            self.podcaster,
            self.special_podcaster,
        }

        assert set(
            self.policy.users_with_any_permission_for_instance(
                ['delete', 'foobar'], self.other_podcast
            )
        ) == {self.superuser, self.manager, self.special_podcaster}

    @pytest.mark.parametrize(
        'user_attr, perms',
        [
            ('superuser', (True, True)),
            ('inactive_superuser', (False, False)),
            ('manager', (True, True)),
            ('main_manager', (True, False)),
            ('podcaster', (True, True)),
            ('main_podcaster', (True, False)),
            ('useless_user', (False, False)),
            ('anonymous_user', (False, False)),
        ],
    )
    def test_user_has_permission_for_radio_show(self, user_attr, perms):
        user = getattr(self, user_attr)
        can_add_main, can_add_other = perms
        assert (
            self.policy.user_has_permission_for_radio_show(
                user, 'add', self.main_show
            )
            is can_add_main
        )
        assert (
            self.policy.user_has_permission_for_radio_show(
                user, 'add', self.other_show
            )
            is can_add_other
        )

    def test_user_has_any_permission_for_radio_show(self):
        assert self.policy.user_has_any_permission_for_radio_show(
            self.main_manager, ['add', 'change'], self.main_show
        )
        assert not self.policy.user_has_any_permission_for_radio_show(
            self.main_manager, ['add', 'change'], self.other_show
        )

        assert self.policy.user_has_any_permission_for_radio_show(
            self.main_podcaster, ['add', 'change'], self.main_show
        )
        assert not self.policy.user_has_any_permission_for_radio_show(
            self.main_podcaster, ['add', 'change'], self.other_show
        )

        assert self.policy.user_has_any_permission_for_radio_show(
            self.special_podcaster, ['add', 'delete'], self.main_show
        )
        assert self.policy.user_has_any_permission_for_radio_show(
            self.special_podcaster, ['add', 'delete'], self.other_show
        )

        assert not self.policy.user_has_any_permission_for_radio_show(
            self.anonymous_user, ['add', 'change'], self.main_show
        )
