from unittest.mock import patch
from urllib.parse import parse_qs

import requests_mock

from django.test import TestCase, override_settings

from allianceauth.analytics.tasks import ANALYTICS_URL
from allianceauth.eveonline.tasks import update_character
from allianceauth.tests.auth_utils import AuthUtils


@override_settings(CELERY_ALWAYS_EAGER=True)
@requests_mock.mock()
class TestAnalyticsForViews(TestCase):
    @override_settings(ANALYTICS_DISABLED=False)
    def test_should_run_analytics(self, requests_mocker):
        # given
        requests_mocker.post(ANALYTICS_URL)
        user = AuthUtils.create_user("Bruce Wayne")
        self.client.force_login(user)
        # when
        response = self.client.get("/dashboard/")
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTrue(requests_mocker.called)

    @override_settings(ANALYTICS_DISABLED=True)
    def test_should_not_run_analytics(self, requests_mocker):
        # given
        requests_mocker.post(ANALYTICS_URL)
        user = AuthUtils.create_user("Bruce Wayne")
        self.client.force_login(user)
        # when
        response = self.client.get("/dashboard/")
        # then
        self.assertEqual(response.status_code, 200)
        self.assertFalse(requests_mocker.called)


@override_settings(CELERY_ALWAYS_EAGER=True)
@requests_mock.mock()
class TestAnalyticsForTasks(TestCase):
    @override_settings(ANALYTICS_DISABLED=False)
    @patch("allianceauth.eveonline.models.EveCharacter.objects.update_character")
    def test_should_run_analytics_for_successful_task(
        self, requests_mocker, mock_update_character
    ):
        # given
        requests_mocker.post(ANALYTICS_URL)
        user = AuthUtils.create_user("Bruce Wayne")
        character = AuthUtils.add_main_character_2(user, "Bruce Wayne", 1001)
        # when
        update_character.delay(character.character_id)
        # then
        self.assertTrue(mock_update_character.called)
        self.assertTrue(requests_mocker.called)
        payload = parse_qs(requests_mocker.last_request.text)
        self.assertListEqual(payload["el"], ["Success"])

    @override_settings(ANALYTICS_DISABLED=True)
    @patch("allianceauth.eveonline.models.EveCharacter.objects.update_character")
    def test_should_not_run_analytics_for_successful_task(
        self, requests_mocker, mock_update_character
    ):
        # given
        requests_mocker.post(ANALYTICS_URL)
        user = AuthUtils.create_user("Bruce Wayne")
        character = AuthUtils.add_main_character_2(user, "Bruce Wayne", 1001)
        # when
        update_character.delay(character.character_id)
        # then
        self.assertTrue(mock_update_character.called)
        self.assertFalse(requests_mocker.called)

    @override_settings(ANALYTICS_DISABLED=False)
    @patch("allianceauth.eveonline.models.EveCharacter.objects.update_character")
    def test_should_run_analytics_for_failed_task(
        self, requests_mocker, mock_update_character
    ):
        # given
        requests_mocker.post(ANALYTICS_URL)
        mock_update_character.side_effect = RuntimeError
        user = AuthUtils.create_user("Bruce Wayne")
        character = AuthUtils.add_main_character_2(user, "Bruce Wayne", 1001)
        # when
        update_character.delay(character.character_id)
        # then
        self.assertTrue(mock_update_character.called)
        self.assertTrue(requests_mocker.called)
        payload = parse_qs(requests_mocker.last_request.text)
        self.assertNotEqual(payload["el"], ["Success"])

    @override_settings(ANALYTICS_DISABLED=True)
    @patch("allianceauth.eveonline.models.EveCharacter.objects.update_character")
    def test_should_not_run_analytics_for_failed_task(
        self, requests_mocker, mock_update_character
    ):
        # given
        requests_mocker.post(ANALYTICS_URL)
        mock_update_character.side_effect = RuntimeError
        user = AuthUtils.create_user("Bruce Wayne")
        character = AuthUtils.add_main_character_2(user, "Bruce Wayne", 1001)
        # when
        update_character.delay(character.character_id)
        # then
        self.assertTrue(mock_update_character.called)
        self.assertFalse(requests_mocker.called)
