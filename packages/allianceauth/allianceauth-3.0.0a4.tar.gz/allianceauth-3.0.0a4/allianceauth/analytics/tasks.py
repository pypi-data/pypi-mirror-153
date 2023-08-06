import requests
import logging
from django.conf import settings
from django.apps import apps
from celery import shared_task
from allianceauth import __version__
from .models import AnalyticsTokens, AnalyticsIdentifier
from .utils import (
    install_stat_addons,
    install_stat_tokens,
    install_stat_users)

logger = logging.getLogger(__name__)

BASE_URL = "https://www.google-analytics.com/"

DEBUG_URL = f"{BASE_URL}debug/collect"
COLLECTION_URL = f"{BASE_URL}collect"

if getattr(settings, "ANALYTICS_ENABLE_DEBUG", False) and settings.DEBUG:
    # Force sending of analytics data during in a debug/test environemt
    # Usefull for developers working on this feature.
    logger.warning(
        "You have 'ANALYTICS_ENABLE_DEBUG' Enabled! "
        "This debug instance will send analytics data!")
    DEBUG_URL = COLLECTION_URL

ANALYTICS_URL = COLLECTION_URL

if settings.DEBUG is True:
    ANALYTICS_URL = DEBUG_URL


def analytics_event(category: str,
                    action: str,
                    label: str,
                    value: int = 0,
                    event_type: str = 'Celery'):
    """
    Send a Google Analytics Event for each token stored
    Includes check for if its enabled/disabled

    Args:
        `category` (str): Celery Namespace
        `action` (str): Task Name
        `label` (str): Optional, Task Success/Exception
        `value` (int): Optional, If bulk, Query size, can be a binary True/False
        `event_type` (str): Optional, Celery or Stats only, Default to Celery
    """
    analyticstokens = AnalyticsTokens.objects.all()
    client_id = AnalyticsIdentifier.objects.get(id=1).identifier.hex
    for token in analyticstokens:
        if event_type == 'Celery':
            allowed = token.send_celery_tasks
        elif event_type == 'Stats':
            allowed = token.send_stats
        else:
            allowed = False

        if allowed is True:
            tracking_id = token.token
            send_ga_tracking_celery_event.s(
                tracking_id=tracking_id,
                client_id=client_id,
                category=category,
                action=action,
                label=label,
                value=value).apply_async(priority=9)


@shared_task()
def analytics_daily_stats():
    """Celery Task: Do not call directly

    Gathers a series of daily statistics and sends analytics events containing them
    """
    users = install_stat_users()
    tokens = install_stat_tokens()
    addons = install_stat_addons()
    logger.debug("Running Daily Analytics Upload")

    analytics_event(category='allianceauth.analytics',
                    action='send_install_stats',
                    label='existence',
                    value=1,
                    event_type='Stats')
    analytics_event(category='allianceauth.analytics',
                    action='send_install_stats',
                    label='users',
                    value=users,
                    event_type='Stats')
    analytics_event(category='allianceauth.analytics',
                    action='send_install_stats',
                    label='tokens',
                    value=tokens,
                    event_type='Stats')
    analytics_event(category='allianceauth.analytics',
                    action='send_install_stats',
                    label='addons',
                    value=addons,
                    event_type='Stats')

    for appconfig in apps.get_app_configs():
        analytics_event(category='allianceauth.analytics',
                        action='send_extension_stats',
                        label=appconfig.label,
                        value=1,
                        event_type='Stats')


@shared_task()
def send_ga_tracking_web_view(
                            tracking_id: str,
                            client_id: str,
                            page: str,
                            title: str,
                            locale: str,
                            useragent: str) -> requests.Response:

    """Celery Task: Do not call directly

    Sends Page View events to GA, Called only via analytics.middleware

    Parameters
    ----------
    `tracking_id` (str): Unique Server Identifier
    `client_id` (str): GA Token
    `page` (str): Page Path
    `title` (str): Page Title
    `locale` (str): Browser Language
    `useragent` (str): Browser UserAgent

    Returns
    -------
    requests.Reponse Object
    """
    headers = {"User-Agent": useragent}

    payload = {
            'v': '1',
            'tid': tracking_id,
            'cid': client_id,
            't': 'pageview',
            'dp': page,
            'dt': title,
            'ul': locale,
            'ua': useragent,
            'aip': 1,
            'an': "allianceauth",
            'av': __version__
            }

    response = requests.post(
                        ANALYTICS_URL, data=payload,
                        timeout=5, headers=headers)
    logger.debug(f"Analytics Page View HTTP{response.status_code}")
    return response


@shared_task()
def send_ga_tracking_celery_event(
                                tracking_id: str,
                                client_id: str,
                                category: str,
                                action: str,
                                label: str,
                                value: int) -> requests.Response:
    """Celery Task: Do not call directly

    Sends Page View events to GA, Called only via analytics.middleware

    Parameters
    ----------
    `tracking_id` (str): Unique Server Identifier
    `client_id` (str): GA Token
    `category` (str): Celery Namespace
    `action` (str): Task Name
    `label` (str): Optional, Task Success/Exception
    `value` (int): Optional, If bulk, Query size, can be a binary True/False

    Returns
    -------
    requests.Reponse Object
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

    payload = {
            'v': '1',
            'tid': tracking_id,
            'cid': client_id,
            't': 'event',
            'ec': category,
            'ea': action,
            'el': label,
            'ev': value,
            'aip': 1,
            'an': "allianceauth",
            'av': __version__
            }

    response = requests.post(
                        ANALYTICS_URL, data=payload,
                        timeout=5, headers=headers)
    logger.debug(f"Analytics Celery/Stats Event HTTP{response.status_code}")
    return response
