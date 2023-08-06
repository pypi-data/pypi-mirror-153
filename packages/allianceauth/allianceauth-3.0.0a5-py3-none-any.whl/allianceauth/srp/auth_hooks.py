from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls
from .managers import SRPManager


class SrpMenu(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(
            self, _('Ship Replacement'),
            'far fa-money-bill-alt fa-fw',
            'srp:management',
            navactive=['srp:']
        )

    def render(self, request):
        if request.user.has_perm('srp.access_srp'):
            app_count = SRPManager.pending_requests_count_for_user(request.user)
            self.count = app_count if app_count and app_count > 0 else None
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return SrpMenu()


@hooks.register('url_hook')
def register_url():
    return UrlHook(urls, 'srp', r'^srp/')
