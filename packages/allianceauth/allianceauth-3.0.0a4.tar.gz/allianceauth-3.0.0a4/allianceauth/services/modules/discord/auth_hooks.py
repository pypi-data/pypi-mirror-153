import logging

from django.contrib.auth.models import User
from django.template.loader import render_to_string

from allianceauth import hooks
from allianceauth.services.hooks import ServicesHook

from .models import DiscordUser
from .urls import urlpatterns
from .utils import LoggerAddTag
from . import tasks, __title__


logger = LoggerAddTag(logging.getLogger(__name__), __title__)

# Default priority for single tasks like update group and sync nickname
SINGLE_TASK_PRIORITY = 3


class DiscordService(ServicesHook):
    """Service for managing a Discord server with Auth"""

    def __init__(self):
        ServicesHook.__init__(self)
        self.urlpatterns = urlpatterns
        self.name = 'discord'
        self.service_ctrl_template = 'services/discord/discord_service_ctrl.html'
        self.access_perm = 'discord.access_discord'
        self.name_format = '{character_name}'

    def delete_user(self, user: User, notify_user: bool = False) -> None:
        if self.user_has_account(user):
            logger.debug('Deleting user %s %s account', user, self.name)
            tasks.delete_user.apply_async(
                kwargs={'user_pk': user.pk, 'notify_user': notify_user},
                priority=SINGLE_TASK_PRIORITY
            )

    def render_services_ctrl(self, request):
        if self.user_has_account(request.user):
            user_has_account = True
            username = request.user.discord.username
            discriminator = request.user.discord.discriminator
            if username and discriminator:
                discord_username = f'{username}#{discriminator}'
            else:
                discord_username = ''
        else:
            discord_username = ''
            user_has_account = False

        return render_to_string(
            self.service_ctrl_template,
            {
                'server_name': DiscordUser.objects.server_name(),
                'user_has_account': user_has_account,
                'discord_username': discord_username
            },
            request=request
        )

    def service_active_for_user(self, user):
        has_perms = user.has_perm(self.access_perm)
        logger.debug("User %s has service permission: %s", user, has_perms)
        return has_perms

    def sync_nickname(self, user):
        logger.debug('Syncing %s nickname for user %s', self.name, user)
        if self.user_has_account(user):
            tasks.update_nickname.apply_async(
                kwargs={
                    'user_pk': user.pk,
                    # since the new nickname is not yet in the DB we need to
                    # provide it manually to the task
                    'nickname': DiscordUser.objects.user_formatted_nick(user)
                },
                priority=SINGLE_TASK_PRIORITY
            )

    def sync_nicknames_bulk(self, users: list):
        """Sync nickname for a list of users in bulk.
        Preferred over sync_nickname(), because it will not break the rate limit
        """
        logger.debug(
            'Syncing %s nicknames in bulk for %d users', self.name, len(users)
        )
        user_pks = [user.pk for user in users]
        tasks.update_nicknames_bulk.delay(user_pks)

    def update_all_groups(self):
        logger.debug('Update all %s groups called', self.name)
        tasks.update_all_groups.delay()

    def update_groups(self, user):
        logger.debug('Processing %s groups for %s', self.name, user)
        if self.user_has_account(user):
            tasks.update_groups.apply_async(
                kwargs={
                    'user_pk': user.pk,
                    # since state changes may not yet be in the DB we need to
                    # provide the new state name manually to the task
                    'state_name': user.profile.state.name
                },
                priority=SINGLE_TASK_PRIORITY
            )

    def update_groups_bulk(self, users: list):
        """Updates groups for a list of users in bulk.
        Preferred over update_groups(), because it will not break the rate limit
        """
        logger.debug(
            'Processing %s groups in bulk for %d users', self.name, len(users)
        )
        user_pks = [user.pk for user in users]
        tasks.update_groups_bulk.delay(user_pks)

    @staticmethod
    def user_has_account(user: User) -> bool:
        result = DiscordUser.objects.user_has_account(user)
        if result:
            logger.debug('User %s has a Discord account', user)
        else:
            logger.debug('User %s does not have a Discord account', user)
        return result

    def validate_user(self, user):
        logger.debug('Validating user %s %s account', user, self.name)
        if self.user_has_account(user) and not self.service_active_for_user(user):
            self.delete_user(user, notify_user=True)


@hooks.register('services_hook')
def register_service():
    return DiscordService()
