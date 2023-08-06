from allianceauth.analytics.tasks import (
    analytics_event,
    send_ga_tracking_celery_event,
    send_ga_tracking_web_view)
from django.test.testcases import TestCase


class TestAnalyticsTasks(TestCase):
    def test_analytics_event(self):
        analytics_event(
                        category='allianceauth.analytics',
                        action='send_tests',
                        label='test',
                        value=1,
                        event_type='Stats')

    def test_send_ga_tracking_web_view_sent(self):
        # This test sends if the event SENDS to google
        # Not if it was successful
        tracking_id = 'UA-186249766-2'
        client_id = 'ab33e241fbf042b6aa77c7655a768af7'
        page = '/index/'
        title = 'Hello World'
        locale = 'en'
        useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        response = send_ga_tracking_web_view(
                                            tracking_id,
                                            client_id,
                                            page,
                                            title,
                                            locale,
                                            useragent)
        self.assertEqual(response.status_code, 200)

    def test_send_ga_tracking_web_view_success(self):
        tracking_id = 'UA-186249766-2'
        client_id = 'ab33e241fbf042b6aa77c7655a768af7'
        page = '/index/'
        title = 'Hello World'
        locale = 'en'
        useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        json_response = send_ga_tracking_web_view(
                                                tracking_id,
                                                client_id,
                                                page,
                                                title,
                                                locale,
                                                useragent).json()
        self.assertTrue(json_response["hitParsingResult"][0]["valid"])

    def test_send_ga_tracking_web_view_invalid_token(self):
        tracking_id = 'UA-IntentionallyBadTrackingID-2'
        client_id = 'ab33e241fbf042b6aa77c7655a768af7'
        page = '/index/'
        title = 'Hello World'
        locale = 'en'
        useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        json_response = send_ga_tracking_web_view(
                                            tracking_id,
                                            client_id,
                                            page,
                                            title,
                                            locale,
                                            useragent).json()
        self.assertFalse(json_response["hitParsingResult"][0]["valid"])
        self.assertEqual(json_response["hitParsingResult"][0]["parserMessage"][1]["description"], "The value provided for parameter 'tid' is invalid. Please see http://goo.gl/a8d4RP#tid for details.")

        # [{'valid': False, 'parserMessage': [{'messageType': 'INFO', 'description': 'IP Address from this hit was anonymized to 1.132.110.0.', 'messageCode': 'VALUE_MODIFIED'}, {'messageType': 'ERROR', 'description': "The value provided for parameter 'tid' is invalid. Please see http://goo.gl/a8d4RP#tid for details.", 'messageCode': 'VALUE_INVALID', 'parameter': 'tid'}], 'hit': '/debug/collect?v=1&tid=UA-IntentionallyBadTrackingID-2&cid=ab33e241fbf042b6aa77c7655a768af7&t=pageview&dp=/index/&dt=Hello World&ul=en&ua=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36&aip=1&an=allianceauth&av=2.9.0a2'}]

    def test_send_ga_tracking_celery_event_sent(self):
        tracking_id = 'UA-186249766-2'
        client_id = 'ab33e241fbf042b6aa77c7655a768af7'
        category = 'test'
        action = 'test'
        label = 'test'
        value = '1'
        response = send_ga_tracking_celery_event(
                                                tracking_id,
                                                client_id,
                                                category,
                                                action,
                                                label,
                                                value)
        self.assertEqual(response.status_code, 200)

    def test_send_ga_tracking_celery_event_success(self):
        tracking_id = 'UA-186249766-2'
        client_id = 'ab33e241fbf042b6aa77c7655a768af7'
        category = 'test'
        action = 'test'
        label = 'test'
        value = '1'
        json_response = send_ga_tracking_celery_event(
                                                    tracking_id,
                                                    client_id,
                                                    category,
                                                    action,
                                                    label,
                                                    value).json()
        self.assertTrue(json_response["hitParsingResult"][0]["valid"])

    def test_send_ga_tracking_celery_event_invalid_token(self):
        tracking_id = 'UA-IntentionallyBadTrackingID-2'
        client_id = 'ab33e241fbf042b6aa77c7655a768af7'
        category = 'test'
        action = 'test'
        label = 'test'
        value = '1'
        json_response = send_ga_tracking_celery_event(
                                                    tracking_id,
                                                    client_id,
                                                    category,
                                                    action,
                                                    label,
                                                    value).json()
        self.assertFalse(json_response["hitParsingResult"][0]["valid"])
        self.assertEqual(json_response["hitParsingResult"][0]["parserMessage"][1]["description"], "The value provided for parameter 'tid' is invalid. Please see http://goo.gl/a8d4RP#tid for details.")

        # [{'valid': False, 'parserMessage': [{'messageType': 'INFO', 'description': 'IP Address from this hit was anonymized to 1.132.110.0.', 'messageCode': 'VALUE_MODIFIED'}, {'messageType': 'ERROR', 'description': "The value provided for parameter 'tid' is invalid. Please see http://goo.gl/a8d4RP#tid for details.", 'messageCode': 'VALUE_INVALID', 'parameter': 'tid'}], 'hit': '/debug/collect?v=1&tid=UA-IntentionallyBadTrackingID-2&cid=ab33e241fbf042b6aa77c7655a768af7&t=pageview&dp=/index/&dt=Hello World&ul=en&ua=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36&aip=1&an=allianceauth&av=2.9.0a2'}]
