from allianceauth.analytics.middleware import AnalyticsMiddleware
from unittest.mock import Mock
from django.http import HttpResponse

from django.test.testcases import TestCase


class TestAnalyticsMiddleware(TestCase):

    def setUp(self):
        self.middleware = AnalyticsMiddleware(HttpResponse)
        self.request = Mock()
        self.request.headers = {
                "User-Agent": "AUTOMATED TEST"
            }
        self.request.path = '/testURL/'
        self.request.session = {}
        self.request.LANGUAGE_CODE = 'en'
        self.response = Mock()
        self.response.content = 'hello world'

    def test_middleware(self):
        response = self.middleware.process_response(self.request, self.response)
        self.assertEqual(self.response, response)
