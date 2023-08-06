from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)


class NightModeRedirectView(View):
    SESSION_VAR = "NIGHT_MODE"

    def get(self, request, *args, **kwargs):
        request.session[self.SESSION_VAR] = not self.night_mode_state(request)
        if not request.user.is_anonymous:
            try:
                request.user.profile.night_mode = request.session[self.SESSION_VAR]
                request.user.profile.save()
            except Exception as e:
                logger.exception(e)

        return HttpResponseRedirect(request.GET.get("next", "/"))

    @classmethod
    def night_mode_state(cls, request):
        try:
            return request.session.get(cls.SESSION_VAR, False)
        except AttributeError:
            # Session is middleware
            # Sometimes request wont have a session attribute
            return False


def Generic500Redirect(request):
    messages.error(
        request,
        "Auth encountered an error processing your request, please try again. "
        "If the error persists, please contact the administrators. (500 Internal Server Error)",
    )
    return redirect("authentication:dashboard")


def Generic404Redirect(request, exception):
    messages.error(
        request,
        "Page does not exist. If you believe this is in error please contact the administrators. "
        "(404 Page Not Found)",
    )
    return redirect("authentication:dashboard")


def Generic403Redirect(request, exception):
    messages.error(
        request,
        "You do not have permission to access the requested page. "
        "If you believe this is in error please contact the administrators. (403 Permission Denied)",
    )
    return redirect("authentication:dashboard")


def Generic400Redirect(request, exception):
    messages.error(
        request,
        "Auth encountered an error processing your request, please try again. "
        "If the error persists, please contact the administrators. (400 Bad Request)",
    )
    return redirect("authentication:dashboard")
