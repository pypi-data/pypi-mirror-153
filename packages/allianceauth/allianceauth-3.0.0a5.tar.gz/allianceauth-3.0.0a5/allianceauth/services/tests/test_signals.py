from copy import deepcopy
from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from allianceauth.authentication.models import State
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils


class ServicesSignalsTestCase(TestCase):
    def setUp(self):
        self.member = AuthUtils.create_user('auth_member', disconnect_signals=True)
        AuthUtils.add_main_character_2(
            self.member, 'Test', 1, 2, 'Test Corp', 'TEST'
        )
        self.none_user = AuthUtils.create_user('none_user', disconnect_signals=True)

    @mock.patch('allianceauth.services.signals.transaction')
    @mock.patch('allianceauth.services.signals.ServicesHook')
    def test_m2m_changed_user_groups(self, services_hook, transaction):
        """
        Test that update_groups hook function is called on user groups change
        """
        svc = mock.Mock()
        svc.update_groups.return_value = None
        svc.validate_user.return_value = None

        services_hook.get_services.return_value = [svc]

        # Overload transaction.on_commit so everything happens synchronously
        transaction.on_commit = lambda fn: fn()

        test_group = Group.objects.create(name="Test group")

        # Act, should trigger m2m change
        self.member.groups.add(test_group)
        self.member.save()

        # Assert
        self.assertTrue(services_hook.get_services.called)

        self.assertTrue(svc.update_groups.called)
        args, kwargs = svc.update_groups.call_args
        self.assertEqual(self.member, args[0])

        self.assertTrue(svc.validate_user.called)
        args, kwargs = svc.validate_user.call_args
        self.assertEqual(self.member, args[0])

    @mock.patch('allianceauth.services.signals.disable_user')
    def test_pre_delete_user(self, disable_user):
        """
        Test that disable_member is called when a user is deleted
        """
        self.none_user.delete()

        self.assertTrue(disable_user.called)
        args, kwargs = disable_user.call_args
        self.assertEqual(self.none_user, args[0])

    @mock.patch('allianceauth.services.signals.disable_user')
    def test_pre_save_user_inactivation(self, disable_user):
        """
        Test a user set inactive has disable_member called
        """
        self.member.is_active = False
        self.member.save()  # Signal Trigger

        self.assertTrue(disable_user.called)
        args, kwargs = disable_user.call_args
        self.assertEqual(self.member, args[0])

    @mock.patch('allianceauth.services.signals.disable_user')
    def test_disable_services_on_loss_of_main_character(self, disable_user):
        """
        Test a user set inactive has disable_member called
        """
        self.member.profile.main_character = None
        self.member.profile.save()  # Signal Trigger

        self.assertTrue(disable_user.called)
        args, kwargs = disable_user.call_args
        self.assertEqual(self.member, args[0])

    @mock.patch('allianceauth.services.signals.transaction')
    @mock.patch('allianceauth.services.signals.ServicesHook')
    def test_m2m_changed_group_permissions(self, services_hook, transaction):
        from django.contrib.contenttypes.models import ContentType
        svc = mock.Mock()
        svc.validate_user.return_value = None
        svc.access_perm = 'auth.access_testsvc'

        services_hook.get_services.return_value = [svc]

        # Overload transaction.on_commit so everything happens synchronously
        transaction.on_commit = lambda fn: fn()

        test_group = Group.objects.create(name="Test group")
        AuthUtils.disconnect_signals()
        self.member.groups.add(test_group)
        AuthUtils.connect_signals()

        ct = ContentType.objects.get(app_label='auth', model='permission')
        perm = Permission.objects.create(name="Test perm", codename="access_testsvc", content_type=ct)
        test_group.permissions.add(perm)

        # Act, should trigger m2m change
        test_group.permissions.remove(perm)

        # Assert
        self.assertTrue(services_hook.get_services.called)

        self.assertTrue(svc.validate_user.called)
        args, kwargs = svc.validate_user.call_args
        self.assertEqual(self.member, args[0])

    @mock.patch('allianceauth.services.signals.transaction')
    @mock.patch('allianceauth.services.signals.ServicesHook')
    def test_m2m_changed_user_permissions(self, services_hook, transaction):
        from django.contrib.contenttypes.models import ContentType
        svc = mock.Mock()
        svc.validate_user.return_value = None
        svc.access_perm = 'auth.access_testsvc'

        services_hook.get_services.return_value = [svc]

        # Overload transaction.on_commit so everything happens synchronously
        transaction.on_commit = lambda fn: fn()

        ct = ContentType.objects.get(app_label='auth', model='permission')
        perm = Permission.objects.create(
            name="Test perm", codename="access_testsvc", content_type=ct
        )
        self.member.user_permissions.add(perm)

        # Act, should trigger m2m change
        self.member.user_permissions.remove(perm)

        # Assert
        self.assertTrue(services_hook.get_services.called)

        self.assertTrue(svc.validate_user.called)
        args, kwargs = svc.validate_user.call_args
        self.assertEqual(self.member, args[0])

    @mock.patch('allianceauth.services.signals.transaction')
    @mock.patch('allianceauth.services.signals.ServicesHook')
    def test_m2m_changed_user_state_permissions(self, services_hook, transaction):
        from django.contrib.contenttypes.models import ContentType
        svc = mock.Mock()
        svc.validate_user.return_value = None
        svc.access_perm = 'auth.access_testsvc'

        services_hook.get_services.return_value = [svc]

        # Overload transaction.on_commit so everything happens synchronously
        transaction.on_commit = lambda fn: fn()

        AuthUtils.disconnect_signals()
        test_state = State.objects.create(name="Test state", priority=150)
        self.member.profile.state = test_state
        self.member.profile.save()
        AuthUtils.connect_signals()

        ct = ContentType.objects.get(app_label='auth', model='permission')
        perm = Permission.objects.create(
            name="Test perm", codename="access_testsvc", content_type=ct
        )
        test_state.permissions.add(perm)

        # Act, should trigger m2m change
        test_state.permissions.remove(perm)

        # Assert
        self.assertTrue(services_hook.get_services.called)

        self.assertTrue(svc.validate_user.called)
        args, kwargs = svc.validate_user.call_args
        self.assertEqual(self.member, args[0])

    @mock.patch('allianceauth.services.signals.ServicesHook')
    def test_state_changed_services_validation_and_groups_update(self, services_hook):
        """Test a user changing state has service accounts validated and groups updated
        """
        svc = mock.Mock()
        svc.validate_user.return_value = None
        svc.update_groups.return_value = None
        svc.access_perm = 'auth.access_testsvc'

        services_hook.get_services.return_value = [svc]

        test_state = State.objects.create(name="Test state", priority=150, public=True)
        self.member.profile.state = test_state
        self.member.profile.save()

        # Assert
        self.assertTrue(services_hook.get_services.called)

        self.assertTrue(svc.validate_user.called)
        args, kwargs = svc.validate_user.call_args
        self.assertEqual(self.member, args[0])

        self.assertTrue(svc.update_groups.called)
        args, kwargs = svc.update_groups.call_args
        self.assertEqual(self.member, args[0])


    @mock.patch('allianceauth.services.signals.ServicesHook')
    def test_state_changed_services_validation_and_groups_update_1(self, services_hook):
        """Test a user changing main has service accounts validated and sync updated
        """
        svc = mock.Mock()
        svc.validate_user.return_value = None
        svc.sync_nickname.return_value = None
        svc.access_perm = 'auth.access_testsvc'

        services_hook.get_services.return_value = [svc]

        new_main = EveCharacter.objects.create(
            character_id=123,
            character_name="Alter Ego",
            corporation_id=987,
            corporation_name="ABC"
        )
        self.member.profile.main_character = new_main
        self.member.profile.save()

        # Assert
        self.assertTrue(services_hook.get_services.called)

        self.assertTrue(svc.validate_user.called)
        args, kwargs = svc.validate_user.call_args
        self.assertEqual(self.member, args[0])

        self.assertTrue(svc.sync_nickname.called)
        args, kwargs = svc.sync_nickname.call_args
        self.assertEqual(self.member, args[0])

    @mock.patch('allianceauth.services.signals.ServicesHook')
    def test_state_changed_services_validation_and_groups_update_2(self, services_hook):
        """Test a user changing main has service does not have accounts validated
        and sync updated if the new main is equal to the old main
        """
        svc = mock.Mock()
        svc.validate_user.return_value = None
        svc.sync_nickname.return_value = None
        svc.access_perm = 'auth.access_testsvc'

        services_hook.get_services.return_value = [svc]

        # this creates a clone of the Django object
        new_main = deepcopy(self.member.profile.main_character)
        self.assertIsNot(new_main, self.member.profile.main_character)
        self.member.profile.main_character = new_main
        self.member.profile.save()

        # Assert
        self.assertFalse(services_hook.get_services.called)
        self.assertFalse(svc.validate_user.called)
        self.assertFalse(svc.sync_nickname.called)
