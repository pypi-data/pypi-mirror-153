from django.contrib.auth.models import Group
from allianceauth.tests.auth_utils import AuthUtils
from ..discord_client.tests import (    # noqa
    TEST_GUILD_ID,
    TEST_USER_ID,
    TEST_USER_NAME,
    TEST_USER_DISCRIMINATOR,
    create_role,
    ROLE_ALPHA,
    ROLE_BRAVO,
    ROLE_CHARLIE,
    ROLE_CHARLIE_2,
    ROLE_MIKE,
    ALL_ROLES,
    create_user_info
)

DEFAULT_AUTH_GROUP = 'Member'
MODULE_PATH = 'allianceauth.services.modules.discord'

TEST_MAIN_NAME = 'Spiderman'
TEST_MAIN_ID = 1005


def add_permissions_to_members():
    permission = AuthUtils.get_permission_by_name('discord.access_discord')
    members = Group.objects.get_or_create(name=DEFAULT_AUTH_GROUP)[0]
    AuthUtils.add_permissions_to_groups([permission], [members])
