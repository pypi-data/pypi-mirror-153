from allianceauth.analytics.models import AnalyticsIdentifier
from django.core.exceptions import ValidationError

from django.test.testcases import TestCase

from uuid import UUID, uuid4


# Identifiers
uuid_1 = "ab33e241fbf042b6aa77c7655a768af7"
uuid_2 = "7aa6bd70701f44729af5e3095ff4b55c"


class TestAnalyticsIdentifier(TestCase):

    def test_identifier_random(self):
        self.assertNotEqual(AnalyticsIdentifier.objects.get(), uuid4)

    def test_identifier_singular(self):
        AnalyticsIdentifier.objects.all().delete()
        AnalyticsIdentifier.objects.create(identifier=uuid_1)
        # Yeah i have multiple asserts here, they all do the same thing
        with self.assertRaises(ValidationError):
            AnalyticsIdentifier.objects.create(identifier=uuid_2)
        self.assertEqual(AnalyticsIdentifier.objects.count(), 1)
        self.assertEqual(AnalyticsIdentifier.objects.get(pk=1).identifier, UUID(uuid_1))
