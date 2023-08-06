import yaml
from typing import Optional

from dnastack.client.collections.client import STANDARD_COLLECTION_SERVICE_TYPE_V1_0, \
    EXPLORER_COLLECTION_SERVICE_TYPE_V1_0
from dnastack.client.service_registry.models import ServiceType
from dnastack.configuration.models import Configuration
from .base import CliTestCase


class TestConfiguration(CliTestCase):
    def test_list_available_properties(self):
        result = self.simple_invoke('config', 'schema')
        self.assertIn('description', result)
        self.assertIsNotNone(result.get('properties'))
        self.assertEqual(result.get('type'), 'object')
