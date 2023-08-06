from unittest.mock import patch, Mock

from requests.exceptions import HTTPError

from django.test import TestCase

from allianceauth.tests.auth_utils import AuthUtils
from allianceauth.groupmanagement.models import ReservedGroupName

from . import (
    TEST_USER_NAME,
    TEST_USER_ID,
    TEST_MAIN_NAME,
    TEST_MAIN_ID,
    MODULE_PATH,
    ROLE_ALPHA,
    ROLE_BRAVO,
    ROLE_CHARLIE,
    ROLE_CHARLIE_2,
    ROLE_MIKE,
)
from ..discord_client import DiscordClient, DiscordApiBackoff
from ..discord_client.tests import create_matched_role
from ..models import DiscordUser
from ..utils import set_logger_to_file


logger = set_logger_to_file(MODULE_PATH + '.models', __file__)


class TestBasicsAndHelpers(TestCase):

    def test_str(self):
        user = AuthUtils.create_user(TEST_USER_NAME)
        discord_user = DiscordUser.objects.create(user=user, uid=TEST_USER_ID)
        expected = 'Peter Parker - 198765432012345678'
        self.assertEqual(str(discord_user), expected)

    def test_repr(self):
        user = AuthUtils.create_user(TEST_USER_NAME)
        discord_user = DiscordUser.objects.create(user=user, uid=TEST_USER_ID)
        expected = 'DiscordUser(user=\'Peter Parker\', uid=198765432012345678)'
        self.assertEqual(repr(discord_user), expected)


@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
class TestUpdateNick(TestCase):

    def setUp(self):
        self.user = AuthUtils.create_user(TEST_USER_NAME)
        self.discord_user = DiscordUser.objects.create(
            user=self.user, uid=TEST_USER_ID
        )

    def test_can_update(self, mock_DiscordClient):
        AuthUtils.add_main_character_2(self.user, TEST_MAIN_NAME, TEST_MAIN_ID)
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        result = self.discord_user.update_nickname()
        self.assertTrue(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_dont_update_if_user_has_no_main(self, mock_DiscordClient):
        mock_DiscordClient.return_value.modify_guild_member.return_value = False

        result = self.discord_user.update_nickname()
        self.assertFalse(result)
        self.assertFalse(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_return_none_if_user_no_longer_a_member(self, mock_DiscordClient):
        AuthUtils.add_main_character_2(self.user, TEST_MAIN_NAME, TEST_MAIN_ID)
        mock_DiscordClient.return_value.modify_guild_member.return_value = None

        result = self.discord_user.update_nickname()
        self.assertIsNone(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_return_false_if_api_returns_false(self, mock_DiscordClient):
        AuthUtils.add_main_character_2(self.user, TEST_MAIN_NAME, TEST_MAIN_ID)
        mock_DiscordClient.return_value.modify_guild_member.return_value = False

        result = self.discord_user.update_nickname()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)


@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
class TestUpdateUsername(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = AuthUtils.create_user(TEST_USER_NAME)

    def setUp(self):
        self.discord_user = DiscordUser.objects.create(
            user=self.user,
            uid=TEST_USER_ID,
            username=TEST_MAIN_NAME,
            discriminator='1234'
        )

    def test_can_update(self, mock_DiscordClient):
        new_username = 'New name'
        new_discriminator = '9876'
        user_info = {
            'user': {
                'id': str(TEST_USER_ID),
                'username': new_username,
                'discriminator': new_discriminator,
            }
        }
        mock_DiscordClient.return_value.guild_member.return_value = user_info

        result = self.discord_user.update_username()
        self.assertTrue(result)
        self.assertTrue(mock_DiscordClient.return_value.guild_member.called)
        self.discord_user.refresh_from_db()
        self.assertEqual(self.discord_user.username, new_username)
        self.assertEqual(self.discord_user.discriminator, new_discriminator)

    def test_return_none_if_user_no_longer_a_member(self, mock_DiscordClient):
        mock_DiscordClient.return_value.guild_member.return_value = None
        result = self.discord_user.update_username()
        self.assertIsNone(result)
        self.assertTrue(mock_DiscordClient.return_value.guild_member.called)

    def test_return_false_if_api_returns_false(self, mock_DiscordClient):
        mock_DiscordClient.return_value.guild_member.return_value = False
        result = self.discord_user.update_username()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.guild_member.called)

    def test_return_false_if_api_returns_corrput_data_1(self, mock_DiscordClient):
        mock_DiscordClient.return_value.guild_member.return_value = {'invalid': True}
        result = self.discord_user.update_username()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.guild_member.called)

    def test_return_false_if_api_returns_corrput_data_2(self, mock_DiscordClient):
        user_info = {
            'user': {
                'id': str(TEST_USER_ID),
                'discriminator': '1234',
            }
        }
        mock_DiscordClient.return_value.guild_member.return_value = user_info
        result = self.discord_user.update_username()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.guild_member.called)

    def test_return_false_if_api_returns_corrput_data_3(self, mock_DiscordClient):
        user_info = {
            'user': {
                'id': str(TEST_USER_ID),
                'username': TEST_USER_NAME,
            }
        }
        mock_DiscordClient.return_value.guild_member.return_value = user_info
        result = self.discord_user.update_username()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.guild_member.called)


@patch(MODULE_PATH + '.models.notify')
@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
class TestDeleteUser(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = AuthUtils.create_user(TEST_USER_NAME)

    def setUp(self):
        self.discord_user = DiscordUser.objects.create(
            user=self.user, uid=TEST_USER_ID
        )

    def test_can_delete_user(self, mock_DiscordClient, mock_notify):
        mock_DiscordClient.return_value.remove_guild_member.return_value = True
        result = self.discord_user.delete_user()
        self.assertTrue(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.remove_guild_member.called)
        self.assertFalse(mock_notify.called)

    def test_can_delete_user_and_notify_user(self, mock_DiscordClient, mock_notify):
        mock_DiscordClient.return_value.remove_guild_member.return_value = True
        result = self.discord_user.delete_user(notify_user=True)
        self.assertTrue(result)
        self.assertTrue(mock_notify.called)

    def test_can_delete_user_when_member_is_unknown(
        self, mock_DiscordClient, mock_notify
    ):
        mock_DiscordClient.return_value.remove_guild_member.return_value = None
        result = self.discord_user.delete_user()
        self.assertTrue(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.remove_guild_member.called)
        self.assertFalse(mock_notify.called)

    def test_return_false_when_api_fails(self, mock_DiscordClient, mock_notify):
        mock_DiscordClient.return_value.remove_guild_member.return_value = False
        result = self.discord_user.delete_user()
        self.assertFalse(result)

    def test_dont_notify_if_user_was_already_deleted_and_return_none(
        self, mock_DiscordClient, mock_notify
    ):
        mock_DiscordClient.return_value.remove_guild_member.return_value = None
        DiscordUser.objects.get(pk=self.discord_user.pk).delete()
        result = self.discord_user.delete_user()
        self.assertIsNone(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.remove_guild_member.called)
        self.assertFalse(mock_notify.called)

    def test_raise_exception_on_api_backoff(
        self, mock_DiscordClient, mock_notify
    ):
        mock_DiscordClient.return_value.remove_guild_member.side_effect = \
            DiscordApiBackoff(999)
        with self.assertRaises(DiscordApiBackoff):
            self.discord_user.delete_user()

    def test_return_false_on_api_backoff_and_exception_handling_on(
        self, mock_DiscordClient, mock_notify
    ):
        mock_DiscordClient.return_value.remove_guild_member.side_effect = \
            DiscordApiBackoff(999)
        result = self.discord_user.delete_user(handle_api_exceptions=True)
        self.assertFalse(result)

    def test_raise_exception_on_http_error(
        self, mock_DiscordClient, mock_notify
    ):
        mock_exception = HTTPError('error')
        mock_exception.response = Mock()
        mock_exception.response.status_code = 500
        mock_DiscordClient.return_value.remove_guild_member.side_effect = \
            mock_exception

        with self.assertRaises(HTTPError):
            self.discord_user.delete_user()

    def test_return_false_on_http_error_and_exception_handling_on(
        self, mock_DiscordClient, mock_notify
    ):
        mock_exception = HTTPError('error')
        mock_exception.response = Mock()
        mock_exception.response.status_code = 500
        mock_DiscordClient.return_value.remove_guild_member.side_effect = \
            mock_exception
        result = self.discord_user.delete_user(handle_api_exceptions=True)
        self.assertFalse(result)


@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
@patch(MODULE_PATH + '.models.DiscordUser.objects.user_group_names')
class TestUpdateGroups(TestCase):

    def setUp(self):
        self.user = AuthUtils.create_user(TEST_USER_NAME)
        self.discord_user = DiscordUser.objects.create(
            user=self.user, uid=TEST_USER_ID
        )
        self.guild_roles = [ROLE_ALPHA, ROLE_BRAVO, ROLE_CHARLIE, ROLE_MIKE]
        self.roles_requested = [
            create_matched_role(ROLE_ALPHA), create_matched_role(ROLE_BRAVO)
        ]

    def test_update_if_needed(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        roles_current = [1]
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.return_value = self.guild_roles
        mock_DiscordClient.return_value.guild_member.return_value = \
            {'roles': roles_current}
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        result = self.discord_user.update_groups()
        self.assertTrue(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.modify_guild_member.call_args
        self.assertEqual(set(kwargs['role_ids']), {1, 2})

    def test_should_update_and_preserve_managed_and_reserved_roles(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        # given
        roles_current = [1, 3, 4, 13]
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.return_value = [
            ROLE_ALPHA, ROLE_BRAVO, ROLE_CHARLIE, ROLE_MIKE, ROLE_CHARLIE_2
        ]
        mock_DiscordClient.return_value.guild_member.return_value = {
            'roles': roles_current
        }
        mock_DiscordClient.return_value.modify_guild_member.return_value = True
        ReservedGroupName.objects.create(
            name="charlie", reason="dummy", created_by="xyz"
        )
        # when
        result = self.discord_user.update_groups()
        # then
        self.assertTrue(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.modify_guild_member.call_args
        self.assertEqual(set(kwargs['role_ids']), {1, 2, 3, 4, 13})

    def test_dont_update_if_not_needed(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        roles_current = [1, 2, 13]
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.return_value = self.guild_roles
        mock_DiscordClient.return_value.guild_member.return_value = \
            {'roles': roles_current}

        result = self.discord_user.update_groups()
        self.assertTrue(result)
        self.assertFalse(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_update_if_user_has_no_roles_on_discord(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        roles_current = []
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.return_value = self.guild_roles
        mock_DiscordClient.return_value.guild_member.return_value = \
            {'roles': roles_current}
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        result = self.discord_user.update_groups()
        self.assertTrue(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.modify_guild_member.call_args
        self.assertEqual(set(kwargs['role_ids']), {1, 2})

    def test_return_none_if_user_no_longer_a_member(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        mock_DiscordClient.return_value.guild_member.return_value = None

        result = self.discord_user.update_groups()
        self.assertIsNone(result)
        self.assertFalse(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_return_false_if_api_returns_false(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        roles_current = [1]
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.return_value = self.guild_roles
        mock_DiscordClient.return_value.guild_member.return_value = \
            {'roles': roles_current}
        mock_DiscordClient.return_value.modify_guild_member.return_value = False

        result = self.discord_user.update_groups()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_raise_exception_if_member_has_unknown_roles(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        roles_current = [99]
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.return_value = self.guild_roles
        mock_DiscordClient.return_value.guild_member.return_value = \
            {'roles': roles_current}
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        with self.assertRaises(RuntimeError):
            self.discord_user.update_groups()

    def test_refresh_guild_roles_user_roles_dont_not_match(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        def my_guild_roles(guild_id, use_cache=True):
            if use_cache:
                return [ROLE_ALPHA, ROLE_BRAVO, ROLE_MIKE]
            else:
                return [ROLE_ALPHA, ROLE_BRAVO, ROLE_CHARLIE, ROLE_MIKE]

        roles_current = [3]
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.side_effect = my_guild_roles
        mock_DiscordClient.return_value.guild_member.return_value = \
            {'roles': roles_current}
        mock_DiscordClient.return_value.modify_guild_member.return_value = True
        result = self.discord_user.update_groups()
        self.assertTrue(result)
        self.assertEqual(mock_DiscordClient.return_value.guild_roles.call_count, 2)

    def test_raise_exception_if_member_info_is_invalid(
        self,
        mock_user_group_names,
        mock_DiscordClient
    ):
        mock_user_group_names.return_value = []
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = self.roles_requested
        mock_DiscordClient.return_value.guild_roles.return_value = self.guild_roles
        mock_DiscordClient.return_value.guild_member.return_value = \
            {'user': 'dummy'}
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        with self.assertRaises(RuntimeError):
            self.discord_user.update_groups()
