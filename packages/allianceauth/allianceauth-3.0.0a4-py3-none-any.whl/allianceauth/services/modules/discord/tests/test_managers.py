from unittest.mock import patch, Mock
import urllib

from requests.exceptions import HTTPError

from django.contrib.auth.models import Group, User
from django.test import TestCase

from allianceauth.tests.auth_utils import AuthUtils

from . import (
    TEST_GUILD_ID,
    TEST_USER_NAME,
    TEST_USER_ID,
    TEST_MAIN_NAME,
    TEST_MAIN_ID,
    MODULE_PATH,
    ROLE_ALPHA,
    ROLE_BRAVO,
    ROLE_CHARLIE,
)
from ..discord_client.tests import create_matched_role
from ..app_settings import (
    DISCORD_APP_ID,
    DISCORD_APP_SECRET,
    DISCORD_CALLBACK_URL,
)
from ..discord_client import DiscordClient, DiscordApiBackoff
from ..models import DiscordUser
from ..utils import set_logger_to_file


logger = set_logger_to_file(MODULE_PATH + '.managers', __file__)


@patch(MODULE_PATH + '.managers.DISCORD_GUILD_ID', TEST_GUILD_ID)
@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
@patch(MODULE_PATH + '.models.DiscordUser.objects._exchange_auth_code_for_token')
@patch(MODULE_PATH + '.models.DiscordUser.objects.user_group_names')
@patch(MODULE_PATH + '.models.DiscordUser.objects.user_formatted_nick')
class TestAddUser(TestCase):

    def setUp(self):
        self.user = AuthUtils.create_user(TEST_USER_NAME)
        self.user_info = {
            'id': TEST_USER_ID,
            'name': TEST_USER_NAME,
            'username': TEST_USER_NAME,
            'discriminator': '1234',
        }
        self.access_token = 'accesstoken'

    def test_can_create_user_no_roles_no_nick(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.return_value = True

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertTrue(result)
        self.assertTrue(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.add_guild_member.call_args
        self.assertEqual(kwargs['guild_id'], TEST_GUILD_ID)
        self.assertEqual(kwargs['user_id'], TEST_USER_ID)
        self.assertEqual(kwargs['access_token'], self.access_token)
        self.assertIsNone(kwargs['role_ids'])
        self.assertIsNone(kwargs['nick'])

    def test_can_create_user_with_roles_no_nick(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        roles = [
            create_matched_role(ROLE_ALPHA),
            create_matched_role(ROLE_BRAVO),
            create_matched_role(ROLE_CHARLIE)
        ]
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = ['a', 'b', 'c']
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = roles
        mock_DiscordClient.return_value.add_guild_member.return_value = True

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertTrue(result)
        self.assertTrue(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.add_guild_member.call_args
        self.assertEqual(kwargs['guild_id'], TEST_GUILD_ID)
        self.assertEqual(kwargs['user_id'], TEST_USER_ID)
        self.assertEqual(kwargs['access_token'], self.access_token)
        self.assertSetEqual(set(kwargs['role_ids']), {1, 2, 3})
        self.assertIsNone(kwargs['nick'])

    def test_can_activate_existing_user_with_roles_no_nick(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        roles = [
            create_matched_role(ROLE_ALPHA),
            create_matched_role(ROLE_BRAVO),
            create_matched_role(ROLE_CHARLIE)
        ]
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = ['a', 'b', 'c']
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = roles
        mock_DiscordClient.return_value.add_guild_member.return_value = None
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertTrue(result)
        self.assertTrue(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.modify_guild_member.call_args
        self.assertEqual(kwargs['guild_id'], TEST_GUILD_ID)
        self.assertEqual(kwargs['user_id'], TEST_USER_ID)
        self.assertSetEqual(set(kwargs['role_ids']), {1, 2, 3})
        self.assertIsNone(kwargs['nick'])

    @patch(MODULE_PATH + '.managers.DISCORD_SYNC_NAMES', True)
    def test_can_create_user_no_roles_with_nick(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = TEST_MAIN_NAME
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.return_value = True

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertTrue(result)
        self.assertTrue(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.add_guild_member.call_args
        self.assertEqual(kwargs['guild_id'], TEST_GUILD_ID)
        self.assertEqual(kwargs['user_id'], TEST_USER_ID)
        self.assertEqual(kwargs['access_token'], self.access_token)
        self.assertIsNone(kwargs['role_ids'])
        self.assertEqual(kwargs['nick'], TEST_MAIN_NAME)

    @patch(MODULE_PATH + '.managers.DISCORD_SYNC_NAMES', True)
    def test_can_activate_existing_user_no_roles_with_nick(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = TEST_MAIN_NAME
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.return_value = None
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertTrue(result)
        self.assertTrue(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.modify_guild_member.call_args
        self.assertEqual(kwargs['guild_id'], TEST_GUILD_ID)
        self.assertEqual(kwargs['user_id'], TEST_USER_ID)
        self.assertIsNone(kwargs['role_ids'])
        self.assertEqual(kwargs['nick'], TEST_MAIN_NAME)

    @patch(MODULE_PATH + '.managers.DISCORD_SYNC_NAMES', False)
    def test_can_create_user_no_roles_and_without_nick_if_turned_off(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = TEST_MAIN_NAME
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.return_value = True

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertTrue(result)
        self.assertTrue(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        args, kwargs = mock_DiscordClient.return_value.add_guild_member.call_args
        self.assertEqual(kwargs['guild_id'], TEST_GUILD_ID)
        self.assertEqual(kwargs['user_id'], TEST_USER_ID)
        self.assertEqual(kwargs['access_token'], self.access_token)
        self.assertIsNone(kwargs['role_ids'])
        self.assertIsNone(kwargs['nick'])

    def test_can_activate_existing_guild_member(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.return_value = None
        mock_DiscordClient.return_value.modify_guild_member.return_value = True

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertTrue(result)
        self.assertTrue(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_can_activate_existing_guild_member_failure(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.return_value = None
        mock_DiscordClient.return_value.modify_guild_member.return_value = False

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertFalse(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_return_false_when_user_creation_fails(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.return_value = False

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertFalse(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)

    def test_return_false_when_on_api_backoff(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_DiscordClient.return_value.add_guild_member.side_effect = \
            DiscordApiBackoff(999)

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertFalse(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)

    def test_return_false_on_http_error(
        self,
        mock_user_formatted_nick,
        mock_user_group_names,
        mock_exchange_auth_code_for_token,
        mock_DiscordClient
    ):
        mock_user_formatted_nick.return_value = None
        mock_user_group_names.return_value = []
        mock_exchange_auth_code_for_token.return_value = self.access_token
        mock_DiscordClient.return_value.current_user.return_value = self.user_info
        mock_DiscordClient.return_value.match_or_create_roles_from_names\
            .return_value = []
        mock_exception = HTTPError('error')
        mock_exception.response = Mock()
        mock_exception.response.status_code = 500
        mock_DiscordClient.return_value.add_guild_member.side_effect = mock_exception

        result = DiscordUser.objects.add_user(self.user, authorization_code='abcdef')
        self.assertFalse(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.add_guild_member.called)


class TestOauthHelpers(TestCase):

    @patch(MODULE_PATH + '.managers.DISCORD_APP_ID', '123456')
    def test_generate_bot_add_url(self):
        bot_add_url = DiscordUser.objects.generate_bot_add_url()

        auth_url = DiscordClient.OAUTH_BASE_URL
        real_bot_add_url = (
            f'{auth_url}?client_id=123456&scope=bot'
            f'&permissions={DiscordUser.objects.BOT_PERMISSIONS}'
        )
        self.assertEqual(bot_add_url, real_bot_add_url)

    def test_generate_oauth_redirect_url(self):
        oauth_url = DiscordUser.objects.generate_oauth_redirect_url()

        self.assertIn(DiscordClient.OAUTH_BASE_URL, oauth_url)
        self.assertIn('+'.join(DiscordUser.objects.SCOPES), oauth_url)
        self.assertIn(DISCORD_APP_ID, oauth_url)
        self.assertIn(urllib.parse.quote_plus(DISCORD_CALLBACK_URL), oauth_url)

    @patch(MODULE_PATH + '.managers.OAuth2Session')
    def test_process_callback_code(self, oauth):
        instance = oauth.return_value
        instance.fetch_token.return_value = {'access_token': 'mywonderfultoken'}

        token = DiscordUser.objects._exchange_auth_code_for_token('12345')

        self.assertTrue(oauth.called)
        args, kwargs = oauth.call_args
        self.assertEqual(args[0], DISCORD_APP_ID)
        self.assertEqual(kwargs['redirect_uri'], DISCORD_CALLBACK_URL)
        self.assertTrue(instance.fetch_token.called)
        args, kwargs = instance.fetch_token.call_args
        self.assertEqual(args[0], DiscordClient.OAUTH_TOKEN_URL)
        self.assertEqual(kwargs['client_secret'], DISCORD_APP_SECRET)
        self.assertEqual(kwargs['code'], '12345')
        self.assertEqual(token, 'mywonderfultoken')


class TestUserFormattedNick(TestCase):

    def setUp(self):
        self.user = AuthUtils.create_user(TEST_USER_NAME)

    def test_return_nick_when_user_has_main(self):
        AuthUtils.add_main_character_2(self.user, TEST_MAIN_NAME, TEST_MAIN_ID)
        result = DiscordUser.objects.user_formatted_nick(self.user)
        expected = TEST_MAIN_NAME
        self.assertEqual(result, expected)

    def test_return_none_if_user_has_no_main(self):
        result = DiscordUser.objects.user_formatted_nick(self.user)
        self.assertIsNone(result)


class TestUserGroupNames(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_1 = Group.objects.create(name='Group 1')
        cls.group_2 = Group.objects.create(name='Group 2')

    def setUp(self):
        self.user = AuthUtils.create_member(TEST_USER_NAME)

    def test_return_groups_and_state_names_for_user(self):
        self.user.groups.add(self.group_1)
        result = DiscordUser.objects.user_group_names(self.user)
        expected = ['Group 1', 'Member']
        self.assertSetEqual(set(result), set(expected))

    def test_return_state_only_if_user_has_no_groups(self):
        result = DiscordUser.objects.user_group_names(self.user)
        expected = ['Member']
        self.assertSetEqual(set(result), set(expected))


class TestUserHasAccount(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = AuthUtils.create_user(TEST_USER_NAME)

    def test_return_true_if_user_has_account(self):
        DiscordUser.objects.create(user=self.user, uid=TEST_USER_ID)
        self.assertTrue(DiscordUser.objects.user_has_account(self.user))

    def test_return_false_if_user_has_no_account(self):
        self.assertFalse(DiscordUser.objects.user_has_account(self.user))

    def test_return_false_if_user_does_not_exist(self):
        my_user = User(username='Dummy')
        self.assertFalse(DiscordUser.objects.user_has_account(my_user))

    def test_return_false_if_not_called_with_user_object(self):
        self.assertFalse(DiscordUser.objects.user_has_account('abc'))


@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
@patch(MODULE_PATH + '.managers.logger')
class TestServerName(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = AuthUtils.create_user(TEST_USER_NAME)

    def test_returns_name_when_api_returns_it(self, mock_logger, mock_DiscordClient):
        server_name = "El Dorado"
        mock_DiscordClient.return_value.guild_name.return_value = server_name

        self.assertEqual(DiscordUser.objects.server_name(), server_name)
        self.assertFalse(mock_logger.warning.called)

    def test_returns_empty_string_when_api_throws_http_error(
        self, mock_logger, mock_DiscordClient
    ):
        mock_exception = HTTPError('Test exception')
        mock_exception.response = Mock(**{"status_code": 440})
        mock_DiscordClient.return_value.guild_name.side_effect = mock_exception

        self.assertEqual(DiscordUser.objects.server_name(), "")
        self.assertFalse(mock_logger.warning.called)

    def test_returns_empty_string_when_api_throws_service_error(
        self, mock_logger, mock_DiscordClient
    ):
        mock_DiscordClient.return_value.guild_name.side_effect = DiscordApiBackoff(1000)

        self.assertEqual(DiscordUser.objects.server_name(), "")
        self.assertFalse(mock_logger.warning.called)

    def test_returns_empty_string_when_api_throws_unexpected_error(
        self, mock_logger, mock_DiscordClient
    ):
        mock_DiscordClient.return_value.guild_name.side_effect = RuntimeError

        self.assertEqual(DiscordUser.objects.server_name(), "")
        self.assertTrue(mock_logger.warning.called)


@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
class TestRoleForGroup(TestCase):
    def test_return_role_if_found(self, mock_DiscordClient):
        mock_DiscordClient.return_value.match_role_from_name.return_value = ROLE_ALPHA

        group = Group.objects.create(name='alpha')
        self.assertEqual(DiscordUser.objects.group_to_role(group), ROLE_ALPHA)

    def test_return_empty_dict_if_not_found(self, mock_DiscordClient):
        mock_DiscordClient.return_value.match_role_from_name.return_value = dict()

        group = Group.objects.create(name='unknown')
        self.assertEqual(DiscordUser.objects.group_to_role(group), dict())
