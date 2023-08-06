from django.utils.translation import gettext_lazy as _

from allianceauth.services.hooks import MenuItemHook, UrlHook
from allianceauth import hooks

from . import urls
from .managers import GroupManager


class GroupManagementMenuItem(MenuItemHook):
    """ This class ensures only authorized users will see the menu entry """

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            text=_("Group Management"),
            classes="fas fa-users-cog fa-fw",
            url_name="groupmanagement:management",
            order=50,
            navactive=[
                "groupmanagement:management",  # group requests view
                "groupmanagement:membership",  # group membership view
                "groupmanagement:audit_log",  # group audit log view
            ],
        )

    def render(self, request):
        if GroupManager.can_manage_groups(request.user):
            app_count = GroupManager.pending_requests_count_for_user(request.user)
            self.count = app_count if app_count and app_count > 0 else None
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return GroupManagementMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "group", r"^groups/")
