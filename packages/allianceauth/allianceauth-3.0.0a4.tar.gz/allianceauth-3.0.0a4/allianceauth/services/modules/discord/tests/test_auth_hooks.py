from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from allianceauth.notifications.models import Notification
from allianceauth.tests.auth_utils import AuthUtils

from . import TEST_USER_NAME, TEST_USER_ID, add_permissions_to_members, MODULE_PATH
from ..auth_hooks import DiscordService
from ..discord_client import DiscordClient
from ..models import DiscordUser
from ..utils import set_logger_to_file


logger = set_logger_to_file(MODULE_PATH + '.auth_hooks', __file__)


@override_settings(CELERY_ALWAYS_EAGER=True)
class TestDiscordService(TestCase):

    def setUp(self):
        self.member = AuthUtils.create_member(TEST_USER_NAME)
        DiscordUser.objects.create(
            user=self.member,
            uid=TEST_USER_ID,
            username=TEST_USER_NAME,
            discriminator='1234'
        )
        self.none_member = AuthUtils.create_user('Lex Luther')
        self.service = DiscordService
        add_permissions_to_members()
        self.factory = RequestFactory()
        Notification.objects.all().delete()

    def test_service_enabled(self):
        service = self.service()
        self.assertTrue(service.service_active_for_user(self.member))
        self.assertFalse(service.service_active_for_user(self.none_member))

    @patch(MODULE_PATH + '.tasks.update_all_groups')
    def test_update_all_groups(self, mock_update_all_groups):
        service = self.service()
        service.update_all_groups()
        self.assertTrue(mock_update_all_groups.delay.called)

    @patch(MODULE_PATH + '.tasks.update_groups_bulk')
    def test_update_groups_bulk(self, mock_update_groups_bulk):
        service = self.service()
        service.update_groups_bulk([self.member])
        self.assertTrue(mock_update_groups_bulk.delay.called)

    @patch(MODULE_PATH + '.tasks.update_groups')
    def test_update_groups_for_member(self, mock_update_groups):
        service = self.service()
        service.update_groups(self.member)
        self.assertTrue(mock_update_groups.apply_async.called)

    @patch(MODULE_PATH + '.tasks.update_groups')
    def test_update_groups_for_none_member(self, mock_update_groups):
        service = self.service()
        service.update_groups(self.none_member)
        self.assertFalse(mock_update_groups.apply_async.called)

    @patch(MODULE_PATH + '.models.notify')
    @patch(MODULE_PATH + '.tasks.DiscordUser')
    @patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
    def test_validate_user(
        self, mock_DiscordClient, mock_DiscordUser, mock_notify
    ):
        mock_DiscordClient.return_value.remove_guild_member.return_value = True

        # Test member is not deleted
        service = self.service()
        service.validate_user(self.member)
        self.assertTrue(DiscordUser.objects.filter(user=self.member).exists())

        # Test none member is deleted
        DiscordUser.objects.create(user=self.none_member, uid=TEST_USER_ID)
        service.validate_user(self.none_member)
        self.assertFalse(DiscordUser.objects.filter(user=self.none_member).exists())

    @patch(MODULE_PATH + '.tasks.update_nickname')
    def test_sync_nickname(self, mock_update_nickname):
        service = self.service()
        service.sync_nickname(self.member)
        self.assertTrue(mock_update_nickname.apply_async.called)

    @patch(MODULE_PATH + '.tasks.update_nicknames_bulk')
    def test_sync_nicknames_bulk(self, mock_update_nicknames_bulk):
        service = self.service()
        service.sync_nicknames_bulk([self.member])
        self.assertTrue(mock_update_nicknames_bulk.delay.called)

    @patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
    def test_delete_user_is_member(self, mock_DiscordClient):
        mock_DiscordClient.return_value.remove_guild_member.return_value = True

        service = self.service()
        service.delete_user(self.member, notify_user=True)

        self.assertTrue(mock_DiscordClient.return_value.remove_guild_member.called)
        self.assertFalse(DiscordUser.objects.filter(user=self.member).exists())
        self.assertTrue(Notification.objects.filter(user=self.member).exists())

    @patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
    def test_delete_user_is_not_member(self, mock_DiscordClient):
        mock_DiscordClient.return_value.remove_guild_member.return_value = True

        service = self.service()
        service.delete_user(self.none_member)

        self.assertFalse(mock_DiscordClient.return_value.remove_guild_member.called)

    @patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
    def test_render_services_ctrl_with_username(self, mock_DiscordClient):
        service = self.service()
        request = self.factory.get('/services/')
        request.user = self.member

        response = service.render_services_ctrl(request)
        self.assertTemplateUsed(service.service_ctrl_template)
        self.assertIn('/discord/reset/', response)
        self.assertIn('/discord/deactivate/', response)

        # Test register becomes available
        self.member.discord.delete()
        self.member.refresh_from_db()
        request.user = self.member
        response = service.render_services_ctrl(request)
        self.assertIn('/discord/activate/', response)

    @patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
    def test_render_services_ctrl_wo_username(self, mock_DiscordClient):
        my_member = AuthUtils.create_member('John Doe')
        DiscordUser.objects.create(user=my_member, uid=111222333)
        service = self.service()
        request = self.factory.get('/services/')
        request.user = my_member

        response = service.render_services_ctrl(request)
        self.assertTemplateUsed(service.service_ctrl_template)
        self.assertIn('/discord/reset/', response)
        self.assertIn('/discord/deactivate/', response)
