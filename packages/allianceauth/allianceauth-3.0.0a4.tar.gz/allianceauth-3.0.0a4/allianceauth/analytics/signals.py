import logging
from celery.signals import task_failure, task_success
from django.conf import settings
from allianceauth.analytics.tasks import analytics_event

logger = logging.getLogger(__name__)


@task_failure.connect
def process_failure_signal(
                        exception, traceback,
                        sender, task_id, signal,
                        args, kwargs, einfo, **kw):
    logger.debug("Celery task_failure signal %s" % sender.__class__.__name__)
    if getattr(settings, "ANALYTICS_DISABLED", False):
        return

    category = sender.__module__

    if 'allianceauth.analytics' not in category:
        if category.endswith(".tasks"):
            category = category[:-6]

        action = sender.__name__

        label = f"{exception.__class__.__name__}"

        analytics_event(category=category,
                        action=action,
                        label=label)


@task_success.connect
def celery_success_signal(sender, result=None, **kw):
    logger.debug("Celery task_success signal %s" % sender.__class__.__name__)
    if getattr(settings, "ANALYTICS_DISABLED", False):
        return

    category = sender.__module__

    if 'allianceauth.analytics' not in category:
        if category.endswith(".tasks"):
            category = category[:-6]

        action = sender.__name__
        label = "Success"

        value = 0
        if isinstance(result, int):
            value = result

        analytics_event(category=category,
                        action=action,
                        label=label,
                        value=value)
